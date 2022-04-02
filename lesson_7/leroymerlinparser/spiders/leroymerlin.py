import scrapy
from scrapy.http import HtmlResponse
from leroymerlinparser.items import LeroymerlinparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['castorama.ru']
    # start_urls = ['http://leroymerlin.ru/']
    # fix_url = 'https://leroymerlin.ru'
    custom_settings = {
        "ITEM_PIPELINES": {'leroymerlinparser.pipelines.LeroymerlinparserPhotosPipeline': 200},
        "IMAGES_STORE": 'photos'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('search')}"]

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-card__name ga-product-card-name']/@href").getall()
        for link in links:
            # print(self.fix_url+link)
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//div[@class='add-to-cart__price js-fixed-panel-trigger']//text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//img[contains (@src, 'image')]/@data-src")
        loader.add_xpath('table', "//div[@class='product-block product-specifications']/dl/dd/text()|"
                                  "//div[@class='product-block product-specifications']/dl/dt/span/text()")
        yield loader.load_item()
