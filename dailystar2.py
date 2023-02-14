#!/usr/bin/env python3
import requests
import json
import lxml.html
# import pprint
import re

def first(el):
    if el is None or len(el) == 0:
        return None
    return el[0]

def extract_metro(html):
    dom = lxml.html.fromstring(html)

    article_body = first(dom.xpath("//article/.//div[@class='article-wrapper']"))

    if article_body is None:
        return {}
    
    # article > div.article-wrapper > div > div.article-body > figure:nth-child(11) > div > div.mod-image > img
    image_containers = article_body.xpath(".//figure[contains(@class, 'in-article-image')]")

    images = []

    for image_container in image_containers:

        image_url = first(image_container.xpath(".//div[@class='mod-image']/img/@data-src | .//div[@class='img-container']/img[@src!='https://dailystar.co.uk/wp-content/themes/dailystar-parent/img/fallback.png']/@src"))
        
        if image_url is None:
            continue

        image_credit = first(image_container.xpath(".//figcaption/span[@class='credit']/text()"))
        # print(image_credit)

        if image_credit is None:
            continue

        matches = re.search(r"\(Image: ([^)]+)\)$", image_credit)
        # print(matches)
        
        if matches:
            image_credit = matches.group(1)
        else:
            image_credit = ""

        images.append({
            "url": image_url,
            "credit": image_credit
        })

    return images

# url = 'https://www.dailystar.co.uk/diet-fitness/fitness-babe-shares-gym-no-29151328'
url = 'https://www.dailystar.co.uk/news/world-news/chinese-coast-guard-uses-military-29205484'

response = requests.get( 
    url,
    headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36" },
)
data = extract_metro(response.text)
print(json.dumps(data))
