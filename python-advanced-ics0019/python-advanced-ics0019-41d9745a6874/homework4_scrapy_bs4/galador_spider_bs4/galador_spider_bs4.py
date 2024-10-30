# -*- coding: utf-8 -*-
"""
Scrape all the graphics cards that are available in www.galador.ee website, using Beautiful Soup for scraping.

@author: aloansberg
"""
import json
import re

import requests
from bs4 import BeautifulSoup

start_url = "https://www.galador.ee/1630-videokaardid?page=1&size=50&sort=asc&vat=1&list=0"

result = []
count = []


def parse(start_urls):
    """
    Making requests to galador.ee to find all the products under class 'product-box' and add the data to dictionary.

    Dictionaries (products) are added to the result (list) variable, where all the info is collected.
    """

    page = requests.get(start_urls)
    soup = BeautifulSoup(page.text, 'html.parser')

    product_list = soup.find_all("div", class_="product-box")

    # loop every page for products
    for product_box in product_list:
        data = {"Name": product_box.find('div', class_='info-block').span.text, 'Price': '', 'Picture href': ''}

        price = product_box.find('div', class_='price-block').text
        data["Price"] = re.sub("[ €]", '', price)

        data["Picture href"] = product_box.find('div', 'image-block').img['src']

        # checking if 'img' tag's attribute 'href' has '/assets/bundles/' in it. If it is then product has no photo.
        if "/assets/bundles/" in data['Picture href']:
            data["Picture href"] = "No photo"

        result.append(data)
        count.append(1)

        # print out how many items are scraped
        print(f"{len(count)} items are scraped.")

    # checking if there is next page
    try:
        next_page = soup.find("li", class_='next').a['href']
        if next_page:
            next_page = "https://www.galador.ee" + next_page
            parse(next_page)
    except:
        print("No more pages")

    # create json file with utf-8 encoding
    with open("graphics_cards_bs4.json", "w", encoding='utf-8') as writeJSON:
        writeJSON.writelines(json.dumps(result, ensure_ascii=False, indent=0))


if __name__ == '__main__':
    parse(start_url)
