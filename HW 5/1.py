import pymongo
import csv
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["task_db"]
collection = db["task_collection"]

with open("task_1_item.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=";")
    data = [row for row in reader]

collection.drop() 
collection.insert_many(data)

def convert_object_id(results):
    for doc in results:
        doc["_id"] = str(doc["_id"])
    return results

def save_to_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def sort_by_salary(collection):
    result = list(collection.find(limit=10).sort({"salary: pymongo.DESCENDING"}))
    print(result)

sort_by_salary(collection)

# Запрос 1: 
result_1 = list(collection.find().sort("salary", -1).limit(10))
result_1 = convert_object_id(result_1)
save_to_file("result_1.json", result_1)

# Запрос 2: 
result_2 = list(collection.find({"age": {"$lt": 30}}).sort("salary", -1).limit(15))
result_2 = convert_object_id(result_2)
save_to_file("result_2.json", result_2)

# Запрос 3: 
city = "Тбилиси"
professions = ["Строитель", "Врач", "Бухгалтер"]
result_3 = list(
    collection.find({"city": city, "job": {"$in": professions}})
    .sort("age", 1)
    .limit(10)
)
result_3 = convert_object_id(result_3)
save_to_file("result_3.json", result_3)

# Запрос 4: 
age_range = {"$gte": 20, "$lte": 45}  
year_range = {"$gte": "2019", "$lte": "2022"} 
salary_condition = {
    "$or": [
        {"salary": {"$gt": "50000", "$lte": "75000"}},
        {"salary": {"$gt": "125000", "$lt": "150000"}},
    ]
}

result_4_count = collection.count_documents(
    {"age": age_range, "year": year_range, **salary_condition}
)
save_to_file("result_4.json", {"count": result_4_count})
