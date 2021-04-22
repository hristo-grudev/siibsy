import scrapy


class SiibsyItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
