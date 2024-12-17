import csv
import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["banking_db"]
collection = db["banking"]

collection.delete_many({})

with open("banking.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    csv_data = [row for row in csv_reader]
    for row in csv_data:
        row["age"] = int(row["age"])
        row["duration"] = int(row["duration"])
        row["campaign"] = int(row["campaign"])
        row["pdays"] = int(row["pdays"])
        row["previous"] = int(row["previous"])
        row["emp_var_rate"] = float(row["emp_var_rate"])
        row["cons_price_idx"] = float(row["cons_price_idx"])
        row["cons_conf_idx"] = float(row["cons_conf_idx"])
        row["euribor3m"] = float(row["euribor3m"])
        row["nr_employed"] = float(row["nr_employed"])
        row["y"] = int(row["y"])
    collection.insert_many(csv_data)

with open("banking.json", "r") as json_file:
    json_data = [json.loads(line) for line in json_file]
    collection.insert_many(json_data)

# Простая выборка

# 1. Найти все записи с возрастом старше 50 лет
with open("selection 1.json", "w") as file:
    json.dump(list(collection.find({"age": {"$gt": 50}})), file, default=str)

# 2. Найти всех клиентов с образованием "university.degree"
with open("selection 2.json", "w") as file:
    json.dump(list(collection.find({"education": "university.degree"})), file, default=str)

# 3. Найти всех клиентов, у которых был успешный исход предыдущего маркетинга
with open("selection 3.json", "w") as file:
    json.dump(list(collection.find({"poutcome": "success"})), file, default=str)

# 4. Найти всех клиентов, которые имеют кредиты на жилье и кредиты на покупку
with open("selection 4.json", "w") as file:
    json.dump(list(collection.find({"housing": "yes", "loan": "yes"})), file, default=str)

# 5. Найти все записи, где количество кампаний больше 5
with open("selection 5.json", "w") as file:
    json.dump(list(collection.find({"campaign": {"$gt": 5}})), file, default=str)

# Выборка с агрегацией

# 1. Подсчитать количество клиентов с каждым уровнем образования
with open("selection with aggregation 1.json", "w") as file:
    json.dump(list(collection.aggregate([{"$group": {"_id": "$education", "count": {"$sum": 1}}}])), file, default=str)

# 2. Найти средний возраст клиентов по типу работы
with open("selection with aggregation 2.json", "w") as file:
    json.dump(list(collection.aggregate([{"$group": {"_id": "$job", "average_age": {"$avg": "$age"}}}])), file, default=str)

# 3. Найти максимальную продолжительность звонка по каждому месяцу
with open("selection with aggregation 3.json", "w") as file:
    json.dump(list(collection.aggregate([{"$group": {"_id": "$month", "max_duration": {"$max": "$duration"}}}])), file, default=str)

# 4. Найти общее число успешных (y = 1) и неуспешных (y = 0) звонков
with open("selection with aggregation 4.json", "w") as file:
    json.dump(list(collection.aggregate([{"$group": {"_id": "$y", "count": {"$sum": 1}}}])), file, default=str)

# 5. Вычислить среднюю стоимость показателя "euribor3m" по каждому уровню занятости
with open("selection with aggregation 5.json", "w") as file:
    json.dump(list(collection.aggregate([{"$group": {"_id": "$job", "average_euribor3m": {"$avg": "$euribor3m"}}}])), file, default=str)

# Обновление/удаление данных 

# 1. Установить значение поля "default" в "unknown" для всех записей, где оно пустое
collection.update_many({"default": ""}, {"$set": {"default": "unknown"}})

# 2. Увеличить возраст всех клиентов на 1 год
collection.update_many({}, {"$inc": {"age": 1}})

# 3. Удалить все записи с нулевым значением продолжительности звонка
collection.delete_many({"duration": 0})

# 4. Обновить тип контакта на "email" для всех, кто был доступен через "cellular"
collection.update_many({"contact": "cellular"}, {"$set": {"contact": "email"}})

# 5. Удалить все записи, где исход предыдущего маркетинга равен "failure"
collection.delete_many({"poutcome": "failure"})


