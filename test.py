import requests

if __name__ == '__main__':
    response = requests.get('https://bck.hermes.com/product?locale=jp_ja&productsku=H363791S%2008',
                            headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Referer': 'https://www.hermes.com/',
'Origin': 'https://www.hermes.com',
'Connection': 'keep-alive',
'Cookie': '_gcl_au=1.1.2069593077.1734018608; _ga_Y862HCHCQ7=GS1.1.1734018628.1.1.1734018733.23.0.0; datadome=tGlKgiqEhbdjFp9tXQWobYbw30SzuTNzNOB39Ep4h9w~~kgbti3c~4S0o3tnFKfePEeGWKatiLVZTUbyiKsLP8UrWpFIhmvc1L9xFTjEMAB~3xIR09G~LirEdI_tkwxH; __cf_bm=Otpvg6mOep.jS7TcA9BhELjrifF0rCycfR3h9DxLDok-1734018625-1.0.1.1-JkFFiYort141YHmPEAFpkvckj13lEHC8DiFfGKTn3jEXpXVCeDrtckD0C6xFN7WsKzZDy7EQzW5Dj6QkClpFMw; _cs_mk=0.521113062464763_1734018628258; _ga=GA1.1.262694573.1734018628; _yjsu_yjad=1734018628.ca7b1f1f-d0d0-4cb8-b5de-3eccfd4dfefc; _fbp=fb.1.1734018631956.938535206343399223; ECOM_SESS=kpq47wuq0r76w0bum107satgti; correlation_id=x1tfvku1ktd9va2krc0n5mpdsvkanfrqfcxn9v5ebo62u0er98hprwbedbjx65ur; x-xsrf-token=49ee39f9-25a5-4b70-aad5-f562d8d8f974',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'no-cors',
'Sec-Fetch-Site': 'same-site',
'TE': 'trailers',
'x-xsrf-token': '49ee39f9-25a5-4b70-aad5-f562d8d8f974',
'x-hermes-locale': 'jp_ja',
'Priority': 'u=4',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache'})
    print(f'ci={response.status_code}')
    print(f'ci={response.text}')