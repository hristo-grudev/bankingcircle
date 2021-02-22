import scrapy

from scrapy.loader import ItemLoader
from ..items import BankingcircleItem
from itemloaders.processors import TakeFirst


class BankingcircleSpider(scrapy.Spider):
	name = 'bankingcircle'
	start_urls = ['https://www.bankingcircle.com/news-events']

	def parse(self, response):
		post_links = response.xpath('//footer[@class="entry-footer"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="cell medium-8 large-7 large-offset-1"]//p/text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()|//div[@class="h4 dark-blue no-margin"]/text()').get()

		item = ItemLoader(item=BankingcircleItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
