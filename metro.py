import requests
import json
import lxml.html
import pprint
import re
import sys

def first(el):
    if el is None or len(el) == 0:
        return None
    return el[0]

def extract_metro(html):
    dom = lxml.html.fromstring(html)

    article_body = first(dom.xpath("//article/div[@class='article-body']"))

    if article_body is None:
        return {}

    image_containers = article_body.xpath(".//figure[contains(@class, 'img-container')]")

    images = []

    for image_container in image_containers:

        image_url = first(image_container.xpath(".//div[@class='img-wrap']/img/@data-src | .//div[@class='img-wrap']/img[@src!='https://metro.co.uk/wp-content/themes/metro-parent/img/fallback.png']/@src"))

        if image_url is None:
            continue

        image_credit = first(image_container.xpath(".//figcaption/text()"))

        if image_credit is None:
            continue

        matches = re.search(r"\(Picture: ([^)]+)\)$", image_credit)
        if matches:
            image_credit = matches.group(1)
        else:
            image_credit = ""

        images.append({
            "url": image_url,
            "credit": image_credit
        })

    return images

response = requests.get('https://metro.co.uk/2023/01/01/benedict-cumberbatchs-family-could-owe-barbados-amid-reparations-claims-18023751/')
# response = requests.get('https://www.dailystar.co.uk/')

print(response)
# data = extract_metro(response.text)
#text = sys.stdin.read()
data = extract_metro(response.text)
print(json.dumps(data))