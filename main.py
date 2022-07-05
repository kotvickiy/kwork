#!/usr/bin/env python3
# sudo apt install python3.10-venv chromium-chromedriver feh xvfb --yes
# python3 -m venv lin_venv3104 && . lin_venv3104/bin/activate
# pip install selenium webdriver_manager requests bs4 lxml
# kill $(pgrep -f .vscode-server/bin/) # убить иксы vscode
# ssh-keygen
# ssh-copy-id vladium@myselfserver
# @reboot /usr/bin/sleep 15; ssh vladium@myselfserver Xvfb &
# */5 * * * * cd /home/vladium/kwork/ && /home/vladium/kwork/lin_venv3104/bin/python3 /home/vladium/kwork/main.py >> out.log 2>&1


import csv, os, os.path, glob, time, datetime, re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from telegram_send import send
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
    service = Service("/usr/bin/chromedriver")
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("–no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    driver.set_window_size(800, 4500)
    if not os.path.exists("img/"):
        os.makedirs("img/")
    driver.save_screenshot(f'img/{datetime.datetime.now().strftime("%H:%M:%S %d-%m-%y")}.png')
    response = driver.page_source
    driver.close()
    driver.quit()
    return response


def get_data(html):
    pattern = '[Пп][Аа][Рр][Сс]|[Сс][Кк][Рр][Ии][Пп][Тт]|[Сс][Оо][Бб][Рр][Аа][Тт][Ьь]|[Чч][Ее][Кк][Ее][Рр]|[Бб][Оо][Тт]'
    # pattern = '[Пп][Аа][Рр][Сс]'
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
    for i in range(1, 11):  # проверяем только 10 страниц
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
        for i in freshs_lst:
            send(str(i['name'] + '\n' + i['price'] + '\n' + i['link']))
        freshs_lst.extend(ref_lst[:10])
        save(freshs_lst)


def main():
    try:
        if glob.glob("img/*.png"):
            for f in glob.glob("img/*.png"):
                os.remove(f)
        if os.path.exists('./kwork.csv'):
            verify_news()
        else:
            save(get_data_pages())
    except Exception as ex:
        print(ex)
        

if __name__ == "__main__":
    main()
