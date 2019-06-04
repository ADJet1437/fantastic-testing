import scrapy
from scrapy.http import Request
import dateparser
from datetime import datetime
from your_project.items import NewsItem

class YoutubeSpider(scrapy.spider):
    name = 'youtube'
    allowed_domains = ['youtube.com']

    def start_requests(self):
        start_urls = ['https://www.youtube.com/results?search_query=news']
        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        news = NewsItem() 
        contents = response.xpath("//div[@class='yt-lockup-content']")
        for content in contents:
            url = self.extract(content.xpath(".//a/@href")) # the url for the news
            title = self.extract(content.xpath(".//a/@title")) # news title
            summary = self.extract_all(content.xpath(
                ".//div[@class='yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2']//text()"))
            date_str = self.extract(content.xpath(
                ".//ul[@class='yt-lockup-meta-info']/li[1]/text()"))
            date_time = dateparser.parse(date_str)
            news_date = datetime.strftime(date_time, "%Y-%m-%d")
            publisher = self.extract(content.xpath(
                ".//div[@class='yt-lockup-byline']//a//text()"))
            if not publisher:
                self.go_to_news_page(url)
                publisher = self.get_publisher(response)
            if not publisher:
                publisher = self.extract(content.xpath(
                    '//meta[@name="title"]/@content'))
            # news items defined in item.py file
            news['TestUrl'] = url
            news['TestSummary'] = summary
            news['publisher'] = publisher
            news['TestDateText'] = news_date
            news['TestTitle'] = title

            yield news