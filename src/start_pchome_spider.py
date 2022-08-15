import json

from models.models import Product
from app import db

import requests
from bs4 import BeautifulSoup


def get_sign(link):
    str_list = link.split('/')
    type_name = str_list[-1].replace('.htm', '')
    return f'h24%252F{type_name}'


def get_pchome_type_index_list(sign):
    url = f'https://ecapi2.pchome.com.tw/cdn/ecshop/cateapi/v1.5/region&sign={sign}'
    response = requests.get(url=url)
    if not response:
        raise Exception()
    response_data = json.loads(response.text)
    results = [
        {
            'code': data['Id'],
            'name': data['Name'],
        } for data in response_data
    ]
    return results


def get_menu_list(index):
    callback_pattern = 'jsonp_menu'
    head = 'try{' + callback_pattern + '('
    end = ');}catch(e){if(window.console){console.log(e);}}'
    url = f'https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.6/region/{index}' \
          f'/menu&_callback={callback_pattern}'
    response = requests.get(url=url)
    if not response:
        return []
    response_data = response.text.replace(head, '').replace(end, '')
    response_data = json.loads(response_data)
    results = [data['Id'] for data in response_data]
    return results


def get_img_url(data):
    _IMAGE_DOMAIN = 'https://cs-d.ecimg.tw'
    img_url = data['Pic'].get('B')
    img_url = f'{_IMAGE_DOMAIN}{img_url}' if img_url else None
    return img_url


def get_price(price_dict):
    origin = price_dict.get('M') or 0
    sale = price_dict.get('P') or 0
    return int(origin) or int(sale)


def get_product_list(index):
    count = 30
    callback_pattern = 'jsonp_prodtop'
    head = 'try{' + callback_pattern + '('
    end = ');}catch(e){if(window.console){console.log(e);}}'
    url = f'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/newarrival/{index}/' \
          f'prod&offset=0&limit={count}&' \
          f'fields=Id,Nick,Pic,Price,Name,OriginPrice,isPreOrder24h' f'&_callback=jsonp_prodtop'
    response = requests.get(url=url)
    if not response:
        return []
    response_data = response.text.replace(head, '').replace(end, '')
    response_data = json.loads(response_data)
    results = [
        {
            'code': data['Id'],
            'name': data['Name'],
            'price': get_price(price_dict=data['Price']),
            'img_url': get_img_url(data=data)
        } for data in response_data
    ]
    return results


if __name__ == '__main__':
    pchome_url = 'https://shopping.pchome.com.tw/'
    response = requests.get(url=pchome_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    type_item_list = soup.find_all('li', {'class': 'overlay_roadsign'})
    type_data_list = list()
    for type_item in type_item_list:
        product_list = list()
        a_item = type_item.find('a', {'class': 'sign'})
        name = a_item.getText()
        link = a_item.get('href')
        link = f'https:{link}' if 'https' not in link else link
        sign = get_sign(link=link)
        index_list = get_pchome_type_index_list(sign=sign)
        for index in index_list:
            new_product_list = get_product_list(index=index['code'])
            product_list += new_product_list
        data = {
            'name': name,
            'product_list': product_list
        }
        type_data_list.append(data)

        for datas in type_data_list:
            for data in datas['product_list']:
                product = Product.query.filter(Product.code == data['code']).first()
                if product:
                    continue
                try:
                    print(data['name'])
                    product = Product(
                        type=datas['name'],
                        code=data['code'],
                        name=data['name'],
                        price=data['price'],
                        pic_url=data['img_url'],
                    )
                    db.session.add(product)
                    db.session.commit()
                except Exception as e:
                    continue
