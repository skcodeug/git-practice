import json
import lxml.html
import requests
import pprint
import re


def people_extract(html):

    dom = lxml.html.fromstring(html)

    main_article_root = dom.xpath("//main/section[@id='taxonomysc_1-0']")[0]

    if len(main_article_root) == 0:
        return 'Element not found'

    get_particular_div = main_article_root.xpath(".//div[@class='loc fixedContent']")[0]

    card_containers = get_particular_div.xpath(".//div[@id='three-post__inner_1-0'] | .//div[@id='tax-sc__recirc-list_1-0']")

    return card_containers


get_req_data = requests.get('https://people.com/tag/news/')


def extracted_objects():
    card_containers = people_extract(get_req_data.text)

    extracted = []

    for card_container in card_containers:
        image_container = card_container.xpath(".//a/div[@class='loc card__top']/div[@class='card__media mntl-universal-image card__media universal-image__container']/div[@class='img-placeholder']")
        image_credit_container = card_container.xpath(".//a/div[@class='card__content']")

        extracted.append({
            'image_container': image_container,
            'image_credit_container': image_credit_container
        })

    return extracted


def dict_xpath(dict_obj, xpath, arr):
    for item in dict_obj:
        image_or_credit = item.xpath(xpath)
        arr.extend(image_or_credit)


def image_information():

    extracted = extracted_objects()

    image_dictionary = []
    credit_dictionary = []

    for extract in extracted:
        image_dictionary.extend(extract['image_container'])
        credit_dictionary.extend(extract['image_credit_container'])

    image_urls = []

    dict_xpath(image_dictionary, ".//img/@data-src", image_urls)

    image_credits = []

    dict_xpath(credit_dictionary, ".//div[@class='card__byline mntl-card__byline ']/@data-byline", image_credits)

    image_details = []

    if len(image_credits) == len(image_urls):
        for index in range(0, len(image_urls)):

            match = re.search(r"[^(By )].*$", image_credits[index])

            im_credit = match.group(0)

            image_details.append({
                "image_url": image_urls[index],
                "image_credit": im_credit
            })

    return image_details


data = image_information()
pprint.pprint(json.dumps(data))

