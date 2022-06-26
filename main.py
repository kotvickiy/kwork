#!/usr/bin/env python3
# python3 -m venv lin_venv3104 && . lin_venv3104/bin/activate
# pip install PyVirtualDisplay xvfbwrapper selenium requests bs4 lxml fake_useragent
# sudo apt install chromium-chromedriver xvfb --yes
# Xvfb :99 -ac & export DISPLAY=:99 # включить иксы в фоне
# kill $(pgrep -f .vscode-server/bin/) # убить иксы vscode


import csv
import os.path
from bs4 import BeautifulSoup as bs
from pyvirtualdisplay import Display
from selenium import webdriver
from telegram_send import send
import re
from time import sleep
from random import uniform


def save(data):
    with open('./kwork.csv', 'w'):
        for i in data:
            with open('./kwork.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow((i['name'], i['price'], i['link']))


def lst_old_kwork():
    with open('./kwork.csv', encoding='utf-8') as file:
        order = ['name', 'price', 'link']
        reader = csv.DictReader(file, fieldnames=order)
        return [i for i in reader]


def get_html(url):
    sleep(uniform(0.1, 0.5))
    display = Display(visible=0, size=(1024, 4250))
    display.start()
    opts = webdriver.ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-setuid-sandbox')
    opts.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(options=opts)
    browser.implicitly_wait(10)
    browser.get(url)
    browser.save_screenshot("screenshot.png")
    response = browser.page_source
    browser.close()
    browser.quit()
    display.stop()
    return response


def get_data(html):
    # pattern = '[Пп][Аа][Рр][Сс]|[Сс][Кк][Рр][Ии][Пп][Тт]|[Сс][Оо][Бб][Рр][Аа][Тт][Ьь]|[Чч][Ее][Кк][Ее][Рр]|[Бб][Оо][Тт]'
    pattern = '[Пп][Аа][Рр][Сс]'
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
        try:
            offers = int(block.find('div', class_='query-item__info-wrap').find_all('span')[1].text.split()[-1].strip())
        except:
            offers = 0
        if offers < 3 and (re.search(pattern, name) or re.search(pattern, description)):
            temp_price = block.find('div', class_='wants-card__header-price wants-card__price m-hidden').text.strip().split()
            price = temp_price[-3] + temp_price[-2]
            link = block.find('div', class_='wants-card__header-title').a['href']

            data = {'name': name, 'price': price, 'link': link}
            lst_data.append(data)   
    return lst_data


def get_data_pages():
    lst_data_pages = []
    for i in range(1, 6):  # проверяем только 5 страниц
        link = f'https://kwork.ru/projects?page={i}&a=1'
        lst_data_pages.extend(get_data(get_html(link)))
    return lst_data_pages


def verify_news():
    ref_lst = lst_old_kwork()
    new_lst = get_data_pages()
    freshs_lst = []
    for new in new_lst:
        if new not in ref_lst:
            freshs_lst.append(new)
    if freshs_lst:
        # print(freshs_lst)
        for i in freshs_lst:
            send(str(i['name'] + '\n' + i['price'] + '\n' + i['link']))
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
