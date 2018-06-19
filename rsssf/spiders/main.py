# -*- coding: utf-8 -*-
import re

import scrapy


MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def find_lists(text):
    result = re.findall(r"""\[
                              (?:[\w\s]+\d+(?:\+\d+)?(?:pen)?[\,\;]?\s*)+
                            \]""", text, flags=re.VERBOSE)
    return [r for r in result if not any(month in r.strip("[]").split()[0] for month in MONTHS)
                                 and len(r) > 3]


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
