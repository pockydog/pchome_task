import re

import requests
from bs4 import BeautifulSoup


class PchomeSpider:
    USER_AGENT = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chro'
                      'me/100.0.4896.127 Safari/537.36'
    }
    DOMAIN = 'https://shopping.pchome.com.tw/'
    PATTERN_URL = r'region/(\w\w\w\w)'

    @classmethod
    def get_product_type_url(cls):
        headers = cls.USER_AGENT
        url = cls.DOMAIN
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        extract_product_url = soup.find_all('li', {'class': 'overlay_roadsign'})
        product_url_list = list()
        for _ in extract_product_url:
            product_url = _.find('a').get('href')
            if 'https' not in product_url:
                url = f'https:{product_url}'
                product_url_list.append(url)
        return product_url_list

    @classmethod
    def parse_product_url(cls, categories_url):
        categories_url_list = list()
        for categories in categories_url:
            categories_ = categories.get('href')
            parse = categories_.replace('store', 'region')
            if 'region' not in parse:
                continue
            else:
                url = re.search(cls.PATTERN_URL, parse).group(0)
                categories_url_list.append(url)
        return categories_url_list

    @classmethod
    def get_categories_url(cls):
        headers = cls.USER_AGENT
        url = 'https://24h.pchome.com.tw/sign/food.htm'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        categories_url = soup.find_all('a', {'class': 'prod_img'})
        categories_list = cls.parse_product_url(categories_url=categories_url)
        result = [f'{cls.DOMAIN}{_}' for _ in categories_list]
        return result

    @classmethod
    def get_product_info(cls):
        headers = cls.USER_AGENT
        url = 'https://24h.pchome.com.tw/prod/DBAUFO-A900AQZZ4'
        response = requests.get(url=url, headers=headers)
        print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup)








