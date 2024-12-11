import requests
import os
import sys
import time

PRESSURE_DATA_HOLDER = 'data_hold'
PRESSURE_DATA = os.path.join(PRESSURE_DATA_HOLDER, 'pressure_test.txt')

except_output_1 = lambda e: print('''
%s
%s
''' % (e.__str__(), sys.exc_info()))


def output_content(content):
    os.makedirs(PRESSURE_DATA_HOLDER, exist_ok=True)
    try:
        with open(PRESSURE_DATA, 'a') as f:
            f.write(content)
    except Exception as e:
        except_output_1(e)


def pressure_test():
    count = 0
    os.remove(PRESSURE_DATA)
    for i in range(500):
        URL = 'https://bck.hermes.cn/product?locale=jp_ja&productsku=H056289CC89'
        print('Requesting[%d] %s' % (i, URL))
        response = requests.get(URL, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:13.0) Gecko/13.0 Firefox/13.0',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'pragma': 'no-cache'
        })
        if response.status_code == 200:
            output_content(response.text + "\n")
        else:
            output_content(str(response.status_code) + ':' + response.text + "\n")
            count += 1
        time.sleep(1)

    output_content('Total requests: %d' % count)

if __name__ == '__main__':
    pressure_test()
