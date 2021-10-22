import scrapy
import re
 
class SpiegelLoginSpider(scrapy.Spider):
    name = 'spiegel'
    allowed_domains = ['gruppenkonto.spiegel.de', 'spigel.de']
    start_urls = ['https://gruppenkonto.spiegel.de/anmelden.html']
    
    def parse(self, response): # 发送Post请求获取Cookies
        form_data = {
            'loginform': 'loginform',
            '_csrf': csrf,
            'loginform:targetUrl':'',
            'loginform:requestAccessToken':'',
            'loginform:productid':'',
            'recaptchaTokenHiddenFieldName_loginform':'',
            'loginform:loginname': 'zjh991600@163.com',
            'loginform:password': 'Zjh991600',
            'loginform:loginAutologin_input': 'on',
            'loginform:submit':'',
            'javax.faces.ViewState': 'stateless'
        }
        yield scrapy.FormRequest.from_response(response,formdata=form_data,callback=self.after_login)
        
    def after_login(self,response):  # 验证是否请求成功
        print(re.findall('Guten Tag, Jihao Zhang',response.body.decode()))