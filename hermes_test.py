import json
import os
import re
import sys
import time
from urllib.parse import unquote, quote

from lxml import etree
from requests import session

HOLD_DATA = 'data_hold'
HOST_HOME = 'https://www.hermes.cn'
HOST_DATA = 'https://bck.hermes.cn'
# COUNTRY = 'cn'
# LOCALE = 'cn_zh'

COUNTRY = 'jp'
LOCALE = 'jp_ja'

error_output = lambda rsp: print(f'''A
Status Code: {rsp.status_code}
Content:
{rsp.text}
''')

except_output = lambda e: print(f'''
{e}
{sys.exc_info()}
''')


def output_data(name, content):
    os.makedirs(HOLD_DATA, exist_ok=True)
    try:
        with open(os.path.join(HOLD_DATA, f'{name}.txt'), 'wb') as f:
            f.write(content)
    except Exception as e:
        except_output(e)


def transform_fragment(fragment):
    match = re.search(r'country=(?P<country>\w+)', fragment)
    return fragment.replace(f'country={match.group('country')}', f'country={COUNTRY}') if match else fragment


def main():
    interval = 1
    limit = 100

    for arg in sys.argv:
        if arg.startswith('--interval='):
            interval = int(arg.split('=')[1])
        elif arg.startswith('--limit='):
            limit = int(arg.split('=')[1])

    print(f'Conditions -- Interval: {interval}, Limit: {limit}')

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

    count = 0
    if resp.status_code == 200:
        for href in etree.HTML(resp.text).xpath('//a[@class="category-poster-cta"]/@href'):
            fragment_start = href.find('#')
            if fragment_start == -1:
                continue
            fragment = unquote(href[fragment_start + 1:])
            matches = regex.finditer(fragment)

            if matches:
                print(fragment)
                fragment = transform_fragment(fragment)
                print(f'-->{fragment}')

                page_size = None
                category = None

                for match in matches:
                    page_size = match.group('page_size') if match.group('page_size') is not None else page_size
                    category = match.group('category') if match.group('category') is not None else category

                request_url = f'{prefix_list}{quote(fragment, safe='=/')}/&locale={LOCALE}&category={category.upper()}&sort=relevance&pagesize={page_size}'
                print(f'Request:{request_url}')
                resp = one_session.get(request_url)
                if resp.status_code == 200:
                    output_data(category, resp.content)
                    time.sleep(interval)
                    for item in json.loads(resp.content)['products']['items']:
                        request_url = f'{prefix_detail}{item['sku']}'
                        print(f'Request:{request_url}')
                        resp = one_session.get(request_url)
                        if resp.status_code == 200:
                            output_data(f'{category}_{item['sku']}', resp.content)
                            count += 1
                            if count >= limit:
                                exit(0)
                        else:
                            error_output(resp)
                        time.sleep(interval)
                else:
                    error_output(resp)
                    time.sleep(interval)
    else:
        error_output(resp)


if __name__ == '__main__':
    main()
