import scrapy
from spiegel import items
import copy

import json
import re
import xmltodict

import lxml.html

from urllib.request import Request, urlopen
from fake_useragent import UserAgent

def scrape_html(article_html: str):
    doc = lxml.html.fromstring(article_html)

    ld_content = doc.xpath('string(//script[@type="application/ld+json"]/text())')
    ld = json.loads(ld_content)
    ld_by_type = {ld_entry['@type']: ld_entry for ld_entry in ld}
    news_ld = ld_by_type['NewsArticle']

    settings = json.loads(doc.xpath('string(//script[@type="application/settings+json"]/text())'))
    info = settings['editorial']['info']

    text_node_selector = \
        'main .word-wrap > p,'  \
        'main .word-wrap > h3, ' \
        'main .word-wrap > ul > li, ' \
        'main .word-wrap > ol > li'
    text_nodes = doc.cssselect(text_node_selector)
    text = re.sub(r'\n+', '\n', '\n'.join([node.text_content() for node in text_nodes])).strip()
    return text


class MirrorSpider(scrapy.Spider):
    name = 'mirror'
    allowed_domains = ['spiegel.de']
    start_urls = ['https://gruppenkonto.spiegel.de/anmelden.html']
    data = list()
    id_list = list()

    def parse(self, response):
        csrf = response.xpath("//input[@name='_csrf']/@value").extract_first()
        post_data = {
            'loginform': 'loginform',
            '_csrf': csrf,
            'loginform:targetUrl': 'https://www.spiegel.de/fuermich/',
            'loginform:requestAccessToken': 'true',
            'loginform:productid': '',
            'recaptchaTokenHiddenFieldName_loginform': '',
            'loginform:loginname': 'username',
            'loginform:password': 'password',
            'loginform:loginAutologin_input': 'on',
            'loginform:submit': '',
            'javax.faces.ViewState': 'stateless'
        }
        yield scrapy.FormRequest(
            "https://gruppenkonto.spiegel.de/anmelden.html",
            formdata = post_data,
            callback = self.after_login
        )

    def after_login(self, response):
        with open('mirror.html', 'w+', encoding='utf-8') as f:
            f.write(response.text)
        item = items.SpiegelItem()
        keywords = ['China', 'chinesisch', 'Beijing', 'Peking',
                    'Taiwan', 'Shanghai', 'Tibet', 'Hongkong',
                    'Nanjing', 'Chinese']
        base_url = "https://joda.spiegel.de/joda/spon/search?s={}&p=SP&f=&page={}&max=100&from={}0101&to={}1231&plus=0"
        for word in keywords:
            for i in range(194, 202):
                headers = {
                    "User-Agent": UserAgent().chrome
                }
                j = 0
                url = base_url.format(word, j, i * 10 + 1, (i + 1) * 10)
                request = Request(url, headers=headers)
                response = urlopen(request)
                xml = response.read()
                convert = xmltodict.parse(xml, encoding='utf-8')
                jsonstr = json.dumps(convert, indent=4)
                tmpDict = json.loads(jsonstr)
                while tmpDict['search-result']['hits'] is not None:
                    self.data += tmpDict['search-result']['hits']['dokument']
                    print('搜索词:', word, '搜索年份范围:', str(i * 10), '-', str((i + 1) * 10), '页码:', str(j))
                    for m in tmpDict['search-result']['hits']['dokument']:
                        if "id" in m:
                            if m['id'] not in self.id_list:
                                self.id_list.append(m['id'])
                                item['_id'] = m['id']
                            else:
                                continue
                        else:
                            item['_id'] = ''
                        if "erscheinungsdatum" in m:
                            item['Erscheinungsdatum'] = m['erscheinungsdatum']
                        else:
                            item['Erscheinungsdatum'] = ''
                        if "ueberschrift" in m:
                            item['Ueberschrift'] = m['ueberschrift']
                        else:
                            item['Ueberschrift'] = ''
                        if "vorspann" in m:
                            item['Vorspann'] = m['vorspann']
                        elif "teaserText" in m:
                            item['Vorspann'] = m['teaserText']
                        else:
                            item['Vorspann'] = ''
                        if "channel" in m:
                            item['Channel'] = m['channel']
                        else:
                            item['Channel'] = ''
                        if "seite" in m:
                            item['Seite'] = m['seite']
                        else:
                            item['Seite'] = ''
                        if "epaperkey" in m:
                            item['Epaperkey'] = m['epaperkey']
                        else:
                            item['Epaperkey'] = ''
                        if "score" in m:
                            item['Score'] = m['score']
                        else:
                            item['Score'] = ''
                        yield scrapy.Request(
                            "https://www.spiegel.de/spiegel/print/d-{}.html".format(m['id']),
                            callback=self.article,
                            meta={'item': copy.deepcopy(item)}
                        )
                    j += 1
                    url = base_url.format(word, j, i * 10 + 1, (i + 1) * 10)
                    request = Request(url, headers=headers)
                    response = urlopen(request)
                    xml = response.read()
                    convert = xmltodict.parse(xml, encoding='utf-8')
                    jsonstr = json.dumps(convert, indent=4)
                    tmpDict = json.loads(jsonstr)
    def article(self, response):
        item = response.meta['item']
        info = response.text
        text = scrape_html(info)
        item['Text'] = text
        yield item

