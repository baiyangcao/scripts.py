# -*- coding: UTF-8 -*-
import scrapy

from jinja2 import Environment, FileSystemLoader, select_autoescape
from os import path
from urllib.parse import urljoin


class NotesSpider(scrapy.Spider):
    name = 'Notes'
    start_urls = [
        'https://baiyangcao.github.io/'
    ]
    data = []

    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'md'])
        )

    def parse(self, response):
        for post in response.css('#main-content h1'):
            json = {
                'text': post.css('a::text').extract_first(),
                'url': urljoin(self.start_urls[0], post.css('a::attr("href")').extract_first())
            }
            # yield json
            self.data.append(json)

        next_url = response.css('li.next a::attr("href")').extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def close(self, reason):
        readme_tempalte = self.env.get_template('README.md')
        readme = readme_tempalte.render(notes=self.data)
        readme_name = getattr(self, 'readme', 'READEME.md')
        with open(readme_name, 'w') as file:
            file.write(readme)

        index_template = self.env.get_template('index.html')
        index = index_template.render(notes=self.data)
        index_name = getattr(self, 'index', 'index.html')
        index_path = path.join('docs', index_name)
        with open(index_path, 'w') as file:
            file.write(index)
