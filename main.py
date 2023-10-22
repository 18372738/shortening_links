import os
from urllib.parse import urlsplit
import argparse

import requests
from dotenv import load_dotenv


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('name', nargs='?')
    return parser


def shorten_link(token, url):
    headers = {
        "Authorization" : f"Bearer {token} ",
    }
    user_url = {
        "long_url": url,
    }
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', json=user_url, headers=headers)
    response.raise_for_status()
    bitlink = response.json()["id"]
    return bitlink


def count_clicks(token, url):
    parsed_url = urlsplit(url)
    bitlink = f"{parsed_url.netloc}{parsed_url.path}"
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary', headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, url):
    parsed_url = urlsplit(url)
    bitlink = f"{parsed_url.netloc}{parsed_url.path}"
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}', headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['BITLY_API_TOKEN']
    parser = createParser()
    input_url = parser.parse_args()

    if input_url.name:
        url = f"{input_url.name}"

    if is_bitlink(token, url):
        try:
            clicks_count = count_clicks(token, url)
            print('Количество посещений:', clicks_count, 'раз(а)')
        except requests.exceptions.HTTPError as error:
            print(f"Не верный формат адреса: \n {error}")
    else:
        try:
            bitlink = shorten_link(token, url)
            print('Битлинк', bitlink)
        except requests.exceptions.HTTPError as error:
            print(f"Не верный формат адреса: \n {error}")
