import scrapy
from TrustpilotReviews.items import TrustpilotreviewsItem
from TrustpilotReviews.pipelines import TrustpilotPipeline, DataBase
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sqlalchemy import Integer, String
import time

class AllocineSpider(CrawlSpider):

    name = "allocine"
    allowed_domains = ["fr.trustpilot.com"]


    def __init__(self, brand, *args, **kwargs):
        super(AllocineSpider, self).__init__(*args, **kwargs)
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.brand = brand
        self.start_urls = [f"https://fr.trustpilot.com/review/{brand}?languages=all"]
        self.database = DataBase(f"sqlite:///trustpilot.db")
        self.database.create_table(f'trustpilot_{brand}_T_{self.time}',id_review=String, name=String, locale=String, title=String, review=String,
                                   rating=Integer, published_date=String)


    rules = (
        Rule(LinkExtractor(allow=("https://fr.trustpilot.com/review/",), restrict_css=("a[data-pagination-button-next-link='true']")), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        self.logger.info(f'Parse review from {response.url}')

        reviews = response.css("article")

        for review in reviews:
            item = TrustpilotreviewsItem()
            item['name'] = review.css("span[data-consumer-name-typography='true']::text").get(default='')
            item['locale'] = review.css("div[data-consumer-country-typography='true'] span::text").get(default='')
            item['title'] = review.css("h2::text").get(default='')
            item['review'] = review.css("p[data-service-review-text-typography='true']::text").get(default='')

            try:
                item['rating'] = int(review.css("section div").attrib['data-service-review-rating'])
            except (ValueError, TypeError, KeyError):
                item['rating'] = 0

            item['published_date'] = review.css("time").attrib.get('datetime', '')

            try:
                self.database.add_row(f'trustpilot_{self.brand}_T_{self.time}', id_review=item['name'] + item['published_date'],name=item['name'], locale=item['locale'], title=item['title'], review=item['review'], rating=item['rating'], published_date=item['published_date'])
            except:
                pass


            yield item