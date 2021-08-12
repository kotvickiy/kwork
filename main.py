#region
import requests
from bs4 import BeautifulSoup as bs
import csv
import os
#endregion


def save(data):
    with open('kwork.csv', 'a', encoding='utf-8', newline='') as file:
        order = ['name', 'price', 'link']
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


def get_html(url):
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        return response.status_code


def get_data(html):
    soup = bs(html, 'lxml')
    blocks = soup.find_all('div', class_='card')
    for block in blocks:
        name = block.find('div', class_='wants-card__header-title').text.strip()
        if 'парс' in name or 'Парс' in name:
            temp_price = block.find('div', class_='wants-card__header-price wants-card__price m-hidden').text.strip().split()
            price = temp_price[-3] + temp_price[-2]
            link = block.find('div', class_='wants-card__header-title').a['href']

            data = {'name': name, 'price': price, 'link': link}
            save(data)
        

def get_data_pages():
    for i in range(1, 11):
        url = f'https://kwork.ru/projects?page={i}'
        get_data(get_html(url))
        print(f'page #{i} done!')


def verify_file_projects():
    pass


def main():
    get_data_pages()

if __name__ == "__main__":
    main()
