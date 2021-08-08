from pymongo import MongoClient


# Функция для разделения строки в подстроки по необходимому символу и очистки подстроки от пробелов в начале и в конце
def composition_clean(string):
    clean_list = []
    temp = string.split(',')
    for i in temp:
        clean_list.append(i.strip())
    return clean_list


# функция для вывода результатов в удобном для просмотра виде
def print_result(result, inadmissible):
    for doc in result:
        print("_____________________________________________________")
        print(dict(doc).get('name'))
        print('____________________состав___________________________')
        for i in dict(doc).get('composition'):
            for j in inadmissible:
                if i == j:
                    print(i + "  <---- в составе присудствует не допустимый для вас продукт")
                    break
            print(i)
        print('___________Пищевая ценность________')
        print('Белки: ' + str(dict(dict(doc).get('esl')).get('protein')) + 'г ')
        print('Жиры: ' + str(dict(dict(doc).get('esl')).get('fats')) + 'г ')
        print('Углеводы: ' + str(dict(dict(doc).get('esl')).get('carbohydrates')) + ' г')
        print('Калориность: ' + str(dict(dict(doc).get('esl')).get('calorie')) + ' ккал')
        print('\r\r\r')


# поиск по штрих-коду (возвращает продукт с указанными полями штрих код которого совпадает с barcode)
def barcode_search(collection, inadmissible):
    print("Введите штрих-код продукта")
    barcode = input()
    result = collection.find({'barcode': barcode}, {'composition': 1, '_id': 0, 'name': 1, 'esl': 1})
    print_result(result, inadmissible)


# поиск по названию (возвращает 10 первых продуктов со всеми полями, названия которых начинаются с name. )
def name_search(collection, inadmissible):
    print("Введите нзвание желаемого продукта")
    name = input()
    result = collection.find({'name': {'$regex': '^' + name, '$options': '$i'}}).limit(10)
    print_result(result, inadmissible)


# Выборка продуктов по диапазону значения калорииности
def calorie_search(collection, inadmissible):
    print('Введите минимальное значение калорииности продукта')
    min = float(input())
    print('Введите максимальное значение калорииности продукта')
    max = float(input())
    result = collection.find({'esl.calorie': {'$gte': min, '$lte': max}})
    print_result(result, inadmissible)


# Выборка продуктов по названию и диапазону значения калорииности
def name_calorie_search(collection, inadmissible):
    print('Введите название продукта')
    name = input()
    print('Введите минимальное значение калорииности продукта')
    min = float(input())
    print('Введите максимальное значение калорииности продукта')
    max = float(input())
    result = collection.find({'name': {'$regex': name, '$options': '$i'}, 'esl.calorie': {'$gte': min, '$lte': max}})
    print_result(result, inadmissible)


# поиск по составу продукта
# вернет продукты в составе которых присутствует список необходимых продуктов и отсутствует список недопустимых.
def composition_search(collection, inadmissible):
    print('Введите предпочтительные для вас продукты(через запятую), которые будут присутствовать'
          ' в составе получаемых вами товаров')
    preferred = composition_clean(input())
    result = collection.find({'$and': [{'composition': {'$in': preferred}}, {'composition': {'$nin': inadmissible}}]})
    print_result(result, inadmissible)


def main():
    client = MongoClient('localhost', 27017)
    collection = client.barcode.goods
    print("\r\r\r\r\r\r")
    print("__________ ПРОГРАММА С КОНСОЛЬНЫМ ИНТЕРФЕЙСОМ ДЛЯ ДЕМОНСТРАЦИИ РЕАЛИЗОВАННЫХ ЗАПРОСОВ _________")
    print('\r\r')
    print("Ведите недопустимые для вас продукты через запятую")
    inadmissible = composition_clean(input())
    print("\r\r Для выбора необходимого вида поиска введите код перед названием")
    print(' 1 - поиск по штрихкоду')
    print(' 2 - поиск по названию')
    print(' 3 - поиск по калорииности')
    print(' 4 - поиск по названию и калорииности')
    print(' 5 - поиск по составу товара')
    code = input()
    if code == '1':
        barcode_search(collection, inadmissible)
    elif code == '2':
        name_search(collection, inadmissible)
    elif code == '3':
        calorie_search(collection, inadmissible)
    elif code == '4':
        name_calorie_search(collection, inadmissible)
    elif code == '5':
        composition_search(collection, inadmissible)


if __name__ == '__main__':
    main()
