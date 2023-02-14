import requests
import json
import lxml.html
import pprint
import re
import sys


def elements(el):
    if el is None or len(el) == 0:
        return None
    return el[0]


def extract_standard(html):
    dom = lxml.html.fromstring(html)
    # print(dom)

    section_body = elements(dom.xpath("//div[@id='main']"))
    # print(f"This is the section {section_body}")

    if section_body is None:
        return {}

    image_warps = section_body.xpath(".//figure")
    # print(image_warps)

    images = []

    for image_warp in image_warps:

        image_url = elements(image_warp.xpath(".//div[@class='sc-iOeugr hTUfRq']/amp-img/@src"))
        # print(image_url)

        if image_url is None:
            continue

        image_credit = elements(image_warp.xpath(".//figcaption[@class='sc-jfvxQR hHISsH']/span[3]/text()"))
        # print(image_credit)

        if image_credit is None:
            continue

        # matches = re.search(r"", image_credit)
        # if matches:
        #     image_credit = matches.group(1)
        # else:
        #     image_credit = ""

        images.append({
            "url": image_url,
            "credit": image_credit
        })
        # print(images)

    return images


# response = requests.get('https://www.standard.co.uk/business'business)
response = requests.get('https://www.standard.co.uk/news/uk/what-to-do-flight-delayed-cancelled-options-city-airport-heathrow-gatwick-b1008149.html')
# print(response)
data = extract_standard(response.text)
# text = sys.stdin.read()
print(json.dumps(data))
