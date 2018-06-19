# -*- coding: utf-8 -*-
import re

import scrapy


def find_lists(text):
    return re.findall(r"""\[
                             (?:[^\d\]+\d+(?:pen)?[\,\;]?\s*)+
                          \]""", text, flags=re.VERBOSE)


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['www.rsssf.com']
    start_urls = ['http://www.rsssf.com/']

    def parse(self, response):
        links = response.xpath("//a/@href").extract()

        lists = find_lists(response.text)
        if lists:
            yield {"lists": lists}

        for link in links:
            full_link = response.urljoin(link)
            yield scrapy.Request(full_link)
