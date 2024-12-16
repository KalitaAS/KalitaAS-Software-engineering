import pymongo
import msgpack
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["task_db"]
collection = db["task_collection"]

with open("task_3_item.msgpack", "rb") as file:
    data = msgpack.unpackb(file.read(), raw=False)
    collection.insert_many(data)

collection.update_many({"salary": {"$type": "string"}}, [{"$set": {"salary": {"$toDouble": "$salary"}}}])

# удаление документов по предикату: salary < 25 000 || salary > 175000
collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})

# увеличение возраста (age) всех документов на 1
collection.update_many({}, {"$inc": {"age": 1}})

# поднять зарплату на 5% для произвольно выбранных профессий
selected_jobs = ["Программист", "Продавец"]
collection.update_many({"job": {"$in": selected_jobs}}, {"$mul": {"salary": 1.05}})

# поднять зарплату на 7% для произвольно выбранных городов
selected_cities = ["Валенсия", "Мурсия"]
collection.update_many({"city": {"$in": selected_cities}}, {"$mul": {"salary": 1.07}})

# поднять зарплату на 10% для выборки по сложному предикату
complex_predicate = {
    "$and": [
        {"city": "Самора"},
        {"job": {"$in": ["Менеджер", "Бухгалтер"]}},
        {"age": {"$gte": 30, "$lte": 50}}
    ]
}
collection.update_many(complex_predicate, {"$mul": {"salary": 1.10}})

# удаление записей по произвольному предикату
random_predicate = {"age": {"$gt": 60}}
collection.delete_many(random_predicate)

