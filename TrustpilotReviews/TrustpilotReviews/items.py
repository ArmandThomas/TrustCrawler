# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrustpilotreviewsItem(scrapy.Item):

    #Profile
    name = scrapy.Field()
    locale = scrapy.Field()

    #Review
    title = scrapy.Field()
    review = scrapy.Field()
    rating = scrapy.Field()

    #Date
    published_date = scrapy.Field()

