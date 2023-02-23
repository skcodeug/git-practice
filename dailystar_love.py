#!/usr/bin/env python3

import requests
import json
import lxml.html
# import lxml.etree
import pprint
import re
import sys

def first(el):
    if el is None or len(el) == 0:
        return None
    return el[0]

def extract_daily(html):
    dom = lxml.html.fromstring(html)

    article_body = first(dom.xpath("//div[@class='article-wrapper']"))
    # print(article_body)

    if article_body is None:
        return {}

    image_containers = article_body.xpath(".//figure[@class='in-article-image']")
    #print(image_containers)

    images = []

    for image_container in image_containers:
        # print(lxml.etree.tostring(image_container))

        image_url = first(image_container.xpath(".//div[@class='outer']/div[2]/img/@data-src | .//div[@class='outer']/img[@src!='https://dailystar.co.uk/wp-content/themes/dailystar-parent/img/fallback.png']/@src"))
        #print(image_url)
        # print(lxml.etree.tostring("image_container"))

        if image_url is None:
            continue

        image_credit = first(image_container.xpath(".//figcaption/span[@class='credit']/text()"))
        #print(image_credit)

        if image_credit is None:
             continue

        matches = re.search(r"\(Image: ([^)]+)\)$", image_credit)
        if matches:
             image_credit = matches.group(1)
        else:
             image_credit = ""

        images.append({
              "url": image_url,
              "credit": image_credit
        })

    return images

url = 'https://www.dailystar.co.uk/love-sex/porn-star-1m-penis-shares-29288273'

response = requests.get(
    url,
    headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36" },
)
#print(response)
data = extract_daily(response.text)
# text = sys.stdin.read()
print(json.dumps(data))