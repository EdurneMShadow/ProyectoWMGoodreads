import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import GoodReadsItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

class GoodReadsSpider(CrawlSpider):
    name = 'goodreads'
    allowed_domains = ['goodreads.com']
    start_urls = ['https://www.goodreads.com/book/show/41865.Twilight']
    rules = (
        Rule (
            LinkExtractor(allow=('/review/show/*',)),
                callback="parse_book", follow=False),)

    def parse_book(self, response):
        reviews=[]
        # Creamos un nuevo libro y asignamos los valores extraidos a
        # los campos correspondientes.
        goodreads = GoodReadsItem()
        goodreads['link']  = response.url
        reviews.append(goodreads)
        return reviews
