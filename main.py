#!/usr/bin/env python3
#region
import requests
from bs4 import BeautifulSoup as bs
import csv
import os.path
from send_telegram import send_telegram
#endregion


def save(data):
    with open('./kwork.csv', 'w'):
        for i in data[:20]:
            with open('./kwork.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow((i['name'], i['price'], i['link']))


def lst_old_kwork():
    with open('./kwork.csv', encoding='utf-8') as file:
        order = ['name', 'price', 'link']
        reader = csv.DictReader(file, fieldnames=order)
        return [i for i in reader]


def get_html(url):
    response = requests.get(url)
    if response.ok:
        return response.text
    print(response.status_code)


def get_data(html):
    lst_data = []
    soup = bs(html, 'lxml')
    blocks = soup.find_all('div', class_='card')
    for block in blocks:
        try:
            name = block.find('div', class_='wants-card__header-title').text.strip()
        except:
            name = 'no name'
        try:
            description = block.find('div', class_='js-want-block-toggle-full').text.strip()
        except:
            description = 'no description'
        if 'парс' in name or 'Парс' in name or 'парс' in description or 'Парс' in description:
            temp_price = block.find('div', class_='wants-card__header-price wants-card__price m-hidden').text.strip().split()
            price = temp_price[-3] + temp_price[-2]
            link = block.find('div', class_='wants-card__header-title').a['href']

            data = {'name': name, 'price': price, 'link': link}
            lst_data.append(data)
    
    return lst_data


def get_data_pages():
    lst_data_pages = []
    for i in range(1, 20):
        lst_data_pages.extend(get_data(get_html(f'https://kwork.ru/projects?page={i}')))      

    return lst_data_pages


def verify_news():
    ref_lst = lst_old_kwork()
    new_lst = get_data_pages()
    freshs_lst = []
    for new in new_lst:
        if new not in ref_lst:
            freshs_lst.append(new)
    if freshs_lst:
        for i in freshs_lst:
                    send_telegram(i['name'] + '\n' + i['price'] + '\n' + i['link'])
        freshs_lst.extend(ref_lst)
        save(freshs_lst)


def main():
    try:
        if os.path.exists('./kwork.csv'):
            verify_news()
        else:
            save(get_data_pages())
    except Exception as ex:
        print(ex)
        

if __name__ == "__main__":
    main()
