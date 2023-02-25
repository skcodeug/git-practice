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


def extract_people(html):
    dom = lxml.html.fromstring(html)
    # print(dom)

    article_body = first(dom.xpath('//main[@id="main"]'))
    # print(article_body)

    if article_body is None:
        return {}

    image_warps = article_body.xpath('.//div[@class="loc article-content"]/figure[@id="figure-article_1-0"] | //div[@class="comp article-content mntl-block"]/div/figure')
    # print(image_warps)

    images = []

    for image_warp in image_warps:
        # print(lxml.etree.tostring(image_warp))

        image_url = first(image_warp.xpath('.//div[@class="primary-image__media"]/div[@class="img-placeholder"]/img/@data-src | //div[@class="figure-media"]/div[@class="img-placeholder"]/img/@data-src'))
        # print(image_url)
        # print(lxml.etree.tostring(image_warp))


        if image_url is None:
            continue

        image_credit = first(image_warp.xpath('.//figcaption[@id="primary-image__figcap_1-0"]/span[@class="figure-article-caption-owner"]/text() | //figcaption/span[@class="figure-article-caption-owner"]/text()'))
        # print(image_credit)

        if image_credit is None:
            continue

    #     matches = re.search(r"\([^)]+)\)$", image_credit)
    #     if matches:
    #         image_credit = matches.group(1)
    #     else:
    #         image_credit = ""
    #
        images.append({
            "url": image_url,
            "credit": image_credit
        })
        # print(images)

    return images


response = requests.get('https://people.com/tv/vanderpump-rules-katie-calls-scheana-snake-evil-troll-for-pushing-tom-schwartz-raquel-hookup/')
# print(response)
data = extract_people(response.text)
# text = sys.stdin.read()
print(json.dumps(data))
