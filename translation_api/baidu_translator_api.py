# -*- coding:utf-8 -*-
"""
-------------------------------------------------
Project Name: toolkits
File Name: baidu_translator_api.py
Author: gaoyw
Create Date: 2021/3/29
-------------------------------------------------
"""


def official_demo():
    """
    免费版 1条/s
    说明界面：https://api.fanyi.baidu.com/doc/21
    """
    import requests
    import json
    from hashlib import md5

    # Set your own appid/appkey.
    appid = '20200729000529030'
    appkey = 'ATTEvDOWLO1U5rD8U3ft'

    # 某些人开源代码里面放出来的
    appid = '20181108000231643'
    appkey = 'ZRvY04W6YyMOnUMHXbub'


    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'zh'
    to_lang = 'en'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    query = '中文翻译原始测试语句。'

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = 1435660288
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    print(result)
    # Show response
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    official_demo()
