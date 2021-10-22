from urllib.request import Request, urlopen
from urllib.parse import urlencode
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd
import xmltodict
import json
import re
import requests
import time
import http.cookiejar as cj

headers = {
    "User-Agent": UserAgent().chrome
}

def get_csrf(s):
    response = s.get("https://gruppenkonto.spiegel.de/meinkonto/uebersicht.html", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    csrf = soup.find('input', attrs={"name": "_csrf"}).get("value")
    return csrf

s = requests.session()
s.verify = False
url_login = 'https://gruppenkonto.spiegel.de/anmelden.html'
url = 'https://www.spiegel.de'

headers1 = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'Referer': 'https://gruppenkonto.spiegel.de/',
    'Host': "www.spiegel.de",
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'cross-site',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://gruppenkonto.spiegel.de'
}

csrf = get_csrf(s)
print(csrf)

formdata = {
    'loginform': 'loginform',
    '_csrf': csrf,
    'loginform:targetUrl':'https://www.spiegel.de/fuermich/',
    'loginform:requestAccessToken':'false',
    'loginform:productid':'',
    'recaptchaTokenHiddenFieldName_loginform':'',
    'loginform:loginname': 'zjh991600@163.com',
    'loginform:password': 'Zjh991600',
    'loginform:loginAutologin_input': 'on',
    'loginform:submit':'',
    'javax.faces.ViewState': 'stateless'
}
r = s.post(url_login, data=formdata, headers=headers)
print(r.headers)
print(r.url)
#print(r.text)
print(r.request.body)
with open('front.html', 'w+', encoding='utf-8') as f:
    f.write(r.text)