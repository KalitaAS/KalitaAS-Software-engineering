import pymongo
import json
from bson import ObjectId  
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["task_db"]
collection = db["task_collection"]

with open("task_2_item.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    collection.insert_many(data)

def convert_objectid(results):
    for doc in results:
        if "_id" in doc and isinstance(doc["_id"], ObjectId):  
            doc["_id"] = str(doc["_id"])
    return results

# вывод минимальной, средней, максимальной salary
pipeline_salary = [
    {"$group": {
        "_id": None,
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]
result_salary = convert_objectid(list(collection.aggregate(pipeline_salary)))
print("Минимальная, средняя, максимальная зарплата:")
print(json.dumps(result_salary, ensure_ascii=False, indent=4))

# вывод количества данных по представленным профессиям
pipeline_jobs = [
    {"$group": {
        "_id": "$job",
        "count": {"$sum": 1}
    }}
]
result_jobs = convert_objectid(list(collection.aggregate(pipeline_jobs)))
print("\nКоличество данных по профессиям:")
print(json.dumps(result_jobs, ensure_ascii=False, indent=4))

# вывод минимальной, средней, максимальной salary по городу
pipeline_city_salary = [
    {"$group": {
        "_id": "$city",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]
result_city_salary = convert_objectid(list(collection.aggregate(pipeline_city_salary)))
print("\nМинимальная, средняя, максимальная зарплата по городу:")
print(json.dumps(result_city_salary, ensure_ascii=False, indent=4))

# вывод минимальной, средней, максимальной salary по профессии
pipeline_job_salary = [
    {"$group": {
        "_id": "$job",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]
result_job_salary = convert_objectid(list(collection.aggregate(pipeline_job_salary)))
print("\nМинимальная, средняя, максимальная зарплата по профессии:")
print(json.dumps(result_job_salary, ensure_ascii=False, indent=4))

# вывод минимального, среднего, максимального возраста по городу
pipeline_city_age = [
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
]
result_city_age = convert_objectid(list(collection.aggregate(pipeline_city_age)))
print("\nМинимальный, средний, максимальный возраст по городу:")
print(json.dumps(result_city_age, ensure_ascii=False, indent=4))

# вывод минимального, среднего, максимального возраста по профессии 
pipeline_job_age = [
    {"$group": {
        "_id": "$job",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
]
result_job_age = convert_objectid(list(collection.aggregate(pipeline_job_age)))
print("\nМинимальный, средний, максимальный возраст по профессии:")
print(json.dumps(result_job_age, ensure_ascii=False, indent=4))

# вывод максимальной заработной платы при минимальном возрасте
pipeline_max_salary_min_age = [
    {"$sort": {"age": 1, "salary": -1}},
    {"$limit": 1}
]
result_max_salary_min_age = convert_objectid(list(collection.aggregate(pipeline_max_salary_min_age)))
print("\nМаксимальная зарплата при минимальном возрасте:")
print(json.dumps(result_max_salary_min_age, ensure_ascii=False, indent=4))

# вывод минимальной заработной платы при максимальной возрасте
pipeline_min_salary_max_age = [
    {"$sort": {"age": -1, "salary": 1}},
    {"$limit": 1}
]
result_min_salary_max_age = convert_objectid(list(collection.aggregate(pipeline_min_salary_max_age)))
print("\nМинимальная зарплата при максимальном возрасте:")
print(json.dumps(result_min_salary_max_age, ensure_ascii=False, indent=4))

# возраст по городам с условием salary > 50000, сортировка по avg_age
pipeline_city_age_condition = [
    {"$match": {"salary": {"$gt": 50000}}},
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }},
    {"$sort": {"avg_age": -1}}
]
result_city_age_condition = convert_objectid(list(collection.aggregate(pipeline_city_age_condition)))
print("\nВозраст по городам (salary > 50000), сортировка по avg_age:")
print(json.dumps(result_city_age_condition, ensure_ascii=False, indent=4))

# salary в диапазонах (18 < age < 25 и 50 < age < 65) по городу и профессии
pipeline_salary_ranges = [
    {"$match": {"$or": [{"age": {"$gt": 18, "$lt": 25}}, {"age": {"$gt": 50, "$lt": 65}}]}},
    {"$group": {
        "_id": {"city": "$city", "job": "$job"},
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]
result_salary_ranges = convert_objectid(list(collection.aggregate(pipeline_salary_ranges)))
print("\nSalary в диапазонах возрастов по городу и профессии:")
print(json.dumps(result_salary_ranges, ensure_ascii=False, indent=4))

# произвольный запрос с $match, $group, $sort
pipeline_custom = [
    {"$match": {"year": {"$gte": 2015}}},
    {"$group": {
        "_id": "$job",
        "total_salary": {"$sum": "$salary"},
        "count": {"$sum": 1}
    }},
    {"$sort": {"total_salary": -1}}
]
result_custom = convert_objectid(list(collection.aggregate(pipeline_custom)))
print("\nОбщая salary работников одной профессии с 2015 г.")
print(json.dumps(result_custom, ensure_ascii=False, indent=4))
