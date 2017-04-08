# -*- coding: UTF-8 -*-
import json
import scrapy


class NotesSpider(scrapy.Spider):
    name = 'Notes'
    start_urls = [
        'https://baiyangcao.github.io/'
    ]
    data = []

    def parse(self, response):
        for post in response.css('#main-content h1'):
            json = {
                'text': post.css('a::text').extract_first(),
                'url': post.css('a::attr("href")').extract_first()
            }
            # yield json
            self.data.append(json)

        next_url = response.css('li.next a::attr("href")').extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def close(self, reason):
        filename = getattr(self, 'filename', 'data.json')
        with open(filename, 'w') as file:
            json.dump(self.data, file, ensure_ascii=False)
