import requests
import json
import lxml.html
# import pprint
import re
import sys
# import lxml.etree


def first(el):
    if el is None or len(el) == 0:
        return None
    return el[0]


def extract_ok(html):
    dom = lxml.html.fromstring(html)
    # print(dom)

    article_body = first(dom.xpath('//main/article/div[@class="article-wrapper"]'))
    # print(article_body)

    if article_body is None:
        return {}

    image_warps = article_body.xpath('.//figure[contains(@class, "in-article-image")]')
    # print(image_warps)

    images = []

    for image_warp in image_warps:
        # print(lxml.etree.tostring(image_warp))

        image_url = first(image_warp.xpath('.//div[@class="mod-image"]/img/@data-src'))
        # print(image_url)


        if image_url is None:
            continue

        image_credit = first(image_warp.xpath('.//figcaption[@class="publication-theme-indicator"]/span[2]/text()'))
        # print(image_credit)

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
        # print(images)

    return images


response = requests.get('https://www.ok.co.uk/tv/breaking-love-island-claudia-casey-29284127', headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36" })
# print(response)
data = extract_ok(response.text)
# text = sys.stdin.read()
print(json.dumps(data))
