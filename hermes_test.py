from requests import session
from lxml import etree
from urllib.parse import unquote, quote
import re
import os
import time
import sys
import json

HOLD_DATA = 'data_hold'
HOST_HOME = 'https://www.hermes.cn'
HOST_DATA = 'https://bck.hermes.cn'
# COUNTRY = 'cn'
# LOCALE = 'cn_zh'

COUNTRY = 'jp'
LOCALE = 'jp_ja'

error_output = lambda rsp : print(f'''A
Status Code: {rsp.status_code}
Content:
{resp.text}
''')

except_output = lambda e : print(f'''
{e}
{sys.exc_info()}
''')

def output_data(name, content):
    os.makedirs(HOLD_DATA, exist_ok=True)
    try:
        with open(os.path.join(HOLD_DATA, f'{name}_{int(time.time() * 1000)}.txt'), 'wb') as f:
            f.write(content)
    except Exception as e:
        except_output(e)

def transform_fragment(fragment):
    match = re.search(r'country=(?P<country>\w+)', fragment)
    return fragment.replace(f'country={match.group('country')}', f'country={COUNTRY}') if match else fragment

if __name__ == '__main__':
    one_session = session()
    one_session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:13.0) Gecko/13.0 Firefox/13.0',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'pragma': 'no-cache'
    })
 
    resp = one_session.get(HOST_HOME)

    regex = re.compile(r'(fh_view_size=(?P<page_size>\d+))|(fh_location=--/categories<{(?P<category>\w+)})')
    prefix_list = f'{HOST_DATA}/products?urlParams='
    prefix_detail = f'{HOST_DATA}/product?locale={LOCALE}&productsku='

    if resp.status_code == 200:
        for herf in etree.HTML(resp.text).xpath('//a[@class="category-poster-cta"]/@href'):
            fragment_start = herf.find('#')
            if fragment_start == -1:
                continue
            fragment = unquote(herf[fragment_start + 1:])
            matches = regex.finditer(fragment)
        
            if matches:
                print(fragment)
                fragment=transform_fragment(fragment)
                print(f'-->{fragment}')
            
                page_size = None
                category = None

                for match in matches:
                    page_size = match.group('page_size') if match.group('page_size') is not None else page_size
                    category = match.group('category') if match.group('category') is not None else category

                next = f'{prefix_list}{quote(fragment, safe='=/')}/&locale={LOCALE}&category={category.upper()}&sort=relevance&pagesize={page_size}'
                print(f'Request:{next}')
                resp = one_session.get(next)
                if resp.status_code == 200:
                    output_data(category, resp.content)
                    for item in json.loads(resp.content)['products']['items']:
                        next = f'{prefix_detail}{item['sku']}'
                        print(f'Request:{next}')
                        resp = one_session.get(next)
                        if resp.status_code == 200:
                            output_data(f'{category}_{item['sku']}', resp.content)
                        else:
                            error_output(resp)
                        time.sleep(1)
                    time.sleep(1)
                else:
                    error_output(resp)

    else:
        error_output(resp)