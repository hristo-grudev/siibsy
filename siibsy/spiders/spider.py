import scrapy

from scrapy.loader import ItemLoader

from ..items import SiibsyItem
from itemloaders.processors import TakeFirst


class SiibsySpider(scrapy.Spider):
	name = 'siibsy'
	start_urls = ['https://www.siib.sy/%D8%B9%D9%86-%D8%A7%D9%84%D8%A8%D9%86%D9%83/%D8%A7%D9%84%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D8%A5%D8%B9%D9%84%D8%A7%D9%85%D9%8A/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%84%D8%A8%D9%86%D9%83']

	def parse(self, response):
		post_links = response.xpath('//div[@class="blog-item"]')

		for post in post_links:
			title = post.xpath('.//h2[@class="article-title"]/a/text()').get()
			description = post.xpath('.//section//p//text()[normalize-space()]').getall()
			description = [p.strip() for p in description if '{' not in p]
			description = ' '.join(description).strip()

			item = ItemLoader(item=SiibsyItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)

			yield item.load_item()

		next_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagination", " " ))]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)
