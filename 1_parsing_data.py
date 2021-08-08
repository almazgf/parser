import re
import requests
import time
from bs4 import BeautifulSoup
import json
import validators


# Функция для записи данных в json-файл
def write_json(data_list):
    filename = 'goods.json'
    write_file = open(filename, mode='w', encoding='UTF-8')
    json.dump(data_list, write_file, indent=4, ensure_ascii=False)
    write_file.close()


# Функция для извлечения HTML-страницы по URL
def get_html(url):
    # Задержка запросов, чтобы не нагружать сервер
    time.sleep(3)
    page = requests.get(url, timeout=(10, 10))
    # Проверка результата запроса страницы
    if page.status_code == 200:
        print('Success')
        return page.text
    elif page.status_code == 404:
        print('Not Found!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


# Функция для получения ссылок первого уровня
def getlinks_level_1(url, links_list):
    page = get_html(url)
    soup = BeautifulSoup(page, 'html.parser')
    temp_list = soup.find('table', id="ctl00_ContentPH_GroupsDG").find_all('a')
    link_check(temp_list, links_list)
    return links_list


# Функция для простой проверки ссылок
def link_check(input_links, output_links):
    for i in input_links:
        if validators.url(f'{i.get("href")}'):
            output_links.append(i.get('href'))
    return output_links


# Функция для разделения строки в подстроки по необходимому символу и очистки подстроки от пробелов в начале и в конце
def composition_clean(string, character):
    clean_list = []
    temp = string.split(character)
    for i in temp:
        clean_list.append(i.strip())
    return clean_list


# Функция для получения ссылок второго уровня
def getlinks_level_2(links_level_1, links_list):
    count_request = 0
    b = 0
    for k in links_level_1:
        page = get_html(k)
        soup = BeautifulSoup(page, 'html.parser')
        try:
            temp_list = soup.find('table', id="ctl00_ContentPH_GoodsDG").find_all('a')
        except AttributeError:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!" + k)
            continue
        count_request = count_request + 1
        print(f'{count_request} level_1')
        b = b + 1
        if b == 500:
            break
        i = 3
        while i < len(temp_list):
            links_list.append(temp_list[i])
            i = i + 3
    return links_list


# Функция для получения необходимых данных со страницы
def getrequired_data(links_level_2, links_list):
    count_request = 0
    for i in links_level_2:
        count_request = count_request + 1
        # Ограничение количества запросов
        if count_request == 3000:
            break
        print(f'{count_request} level_2')
        url = ('http://www.goodsmatrix.ru/goods/' + i.text.strip() + '.html')
        if validators.url(f'{url}'):
            soup = BeautifulSoup(get_html(url), 'html.parser')
            try:
                name = soup.find('span', id="ctl00_ContentPH_GoodsName").text
            except AttributeError:
                name = ''
            try:
                barcode = soup.find('span', id="ctl00_ContentPH_BarCodeL").text
            except AttributeError:
                barcode = ''
            try:
                composition = soup.find('span', id="ctl00_ContentPH_Composition").text
            except AttributeError:
                composition = ''
            try:
                comment = soup.find('span', id="ctl00_ContentPH_Comment").text
            except AttributeError:
                comment = ''
            try:
                gost = soup.find('span', id="ctl00_ContentPH_Gost").text
            except AttributeError:
                gost = ''
            try:
                net_mass = soup.find('span', id="ctl00_ContentPH_Net").text
            except AttributeError:
                net_mass = ''
            try:
                keeping_time = soup.find('span', id="ctl00_ContentPH_KeepingTime").text
            except AttributeError:
                keeping_time = ''
            try:
                storage_conditions = soup.find('span', id="ctl00_ContentPH_StoreCond").text
            except AttributeError:
                storage_conditions = ''
            try:
                esl = soup.find('span', id="ctl00_ContentPH_ESL").text
            except AttributeError:
                esl = ''
            try:
                packing_type = soup.find('span', id="ctl00_ContentPH_PackingType").text
            except AttributeError:
                packing_type = ''

            # Очистка строки энергетическая ценность(esl) и обработка исключении IndexError
            clean_esl = re.findall(r'\d*\.\d+|\d+', esl) #!!!! РЕГУЛЯРНОЕ ВЫРАЖЕНИЕ НЕПРАВИЛЬНОЕ ГЛАВНОЕ НЕ ЗАБЫТЬ ИСПРАВИТЬ.
            try:
                protein = clean_esl[0]
            except IndexError:
                protein = 0
            try:
                fats = clean_esl[1]
            except IndexError:
                fats = 0
            try:
                carbohydrates = clean_esl[2]
            except IndexError:
                carbohydrates = 0
            try:
                calorie = clean_esl[3]
            except IndexError:
                calorie = 0

            # объект Python который мы передаем в JSON. Представляет собой ассоциативный массив.
            product = {
                'name': name,
                'barcode': barcode,
                'composition': composition_clean(composition, ","),
                'comment': comment,
                'gost': gost,
                'net_mass': net_mass,
                'keeping_time': keeping_time,
                'storage_conditions': storage_conditions,
                'esl': {
                    'protein': float(protein),
                    'fats': float(fats),
                    'carbohydrates': float(carbohydrates),
                    'calorie': float(calorie)
                },
                'packing_type': packing_type
            }
            links_list.append(product)
        else:
            continue
    return links_list


def main():
    base_url = "http://www.goodsmatrix.ru/GMMap.aspx"
    links_level_1 = []
    getlinks_level_1(base_url, links_level_1)
    links_level_2 = []
    getlinks_level_2(links_level_1, links_level_2)
    required_data = []
    getrequired_data(links_level_2, required_data)
    write_json(required_data)


if __name__ == '__main__':
    main()
