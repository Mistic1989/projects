# -*- coding: utf-8 -*-
"""
Scrape all the graphics cards that are available in www.galador.ee website, using Scrapy.

@author: aloansberg
scrapy runspider galador_spider_scrapy.py
"""
import json
import re
import scrapy

result = []
count = []


class GaladorSpider(scrapy.Spider):
    """All the requests and parsing is made under GaladorSpider class."""
    name = "galador_spider_scrapy"
    # setting the url to crawl from.
    url = "https://www.galador.ee/1630-videokaardid"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }

    def start_requests(self):
        """Setting headers here."""
        yield scrapy.http.Request(self.url, headers=self.headers)

    def parse(self, response):
        """
        Since every product is placed in product-box class, we are passing product-box selector into the response object.
        """
        SET_SELECTOR = '.product-box'
        for product_box in response.css(SET_SELECTOR):
            """The product_box object has its own css method, 
            so we can pass in a selector to locate child elements.
            """
            NAME_SELECTOR = 'div.info-block span::text'
            PRICE_SELECTOR = 'div.price-block ::text'
            IMAGE_SELECTOR = 'div.image-block img ::attr(src)'

            # Checking if 'img' tag's attribute 'href' has '/assets/bundles/' in it. If it is then product has no photo.
            if "/assets/bundles/" in product_box.css(IMAGE_SELECTOR).extract_first():
                data = {
                    'Title': product_box.css(NAME_SELECTOR).extract_first(),
                    'Price': re.sub("[ €]", '', product_box.css(PRICE_SELECTOR).extract_first()),
                    'Picture href': 'No photo'
                }
            else:
                data = {
                    'Title': product_box.css(NAME_SELECTOR).extract_first(),
                    'Price': re.sub("[ €]", '', product_box.css(PRICE_SELECTOR).extract_first()),
                    'Picture href': product_box.css(IMAGE_SELECTOR).extract_first()
                }
            count.append(1)
            result.append(data)
            yield data

        # checking if there is next page
        next_page = response.css('.next a::attr(href)').extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, self.parse, headers=self.headers)

        # create json file with utf-8 encoding
        with open("graphics_cards_scrapy.json", "w", encoding='utf-8') as writeJSON:
            writeJSON.writelines(json.dumps(result, ensure_ascii=False, indent=0))

        # print out how many items are scraped
        print(f"\n\n\n{len(count)} items are scraped.\n\n\n")
