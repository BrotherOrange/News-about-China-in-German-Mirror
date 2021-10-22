import scrapy
import logging

logger = logging.getLogger(__name__)

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        # retl = response.xpath("//div[@class='maincon']//div[@class='main_bot']//h2/text()").extract()
        # print(retl)

        li_list = response.xpath("//div[@class='maincon']//li")
        for li in li_list:
            item = {}
            item['name'] = li.xpath(".//h2/text()").extract_first()
            item['title'] = li.xpath(".//h2//span/text()").extract_first()
            # logging.warning(item)
            logger.warning(item)
            # print(item)
            yield item