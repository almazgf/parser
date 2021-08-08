

from pymongo import MongoClient
import json

# Чтение данных из файла
filename = 'goods.json'
rite_file = open(filename, mode='r', encoding='UTF-8')
list_goods = json.load(rite_file)
rite_file.close()

# Создание бд и добавление данных в бд
client = MongoClient('localhost', 27017)
db = client.barcode
col = db.goods
result = col.insert_many(list_goods)

print(result)




