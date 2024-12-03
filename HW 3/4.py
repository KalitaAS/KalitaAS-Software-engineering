import os
import json
from bs4 import BeautifulSoup
from collections import Counter
import statistics

# Парсинг XML файла
def parse_xml_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "xml")
        items = []
        for clothing in soup.find_all("clothing"):
            item = {tag.name: tag.get_text(strip=True) for tag in clothing.find_all()}
            if 'price' in item:
                item['price'] = int(item['price'])
            if 'rating' in item:
                item['rating'] = float(item['rating'])
            if 'reviews' in item:
                item['reviews'] = int(item['reviews'])
            items.append(item)
        return items

def process_all_files(directory):
    return [item for file_name in os.listdir(directory) if file_name.endswith(".xml")
            for item in parse_xml_file(os.path.join(directory, file_name))]

def save_to_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def sort_data(data, field):
    return sorted(data, key=lambda x: x.get(field, float('inf')))

def filter_data(data, field, value):
    return [item for item in data if item.get(field) == value]

def calculate_statistics(data, field):
    values = [item[field] for item in data if field in item]
    return { "sum": sum(values), "min": min(values), "max": max(values), "mean": statistics.mean(values) if values else None }

def count_frequencies(data, field):
    return Counter(item.get(field, "Unknown") for item in data)

input_directory = "/content/4"  
output_json = "output.json"

data = process_all_files(input_directory)
save_to_json(data, output_json)

sorted_data = sort_data(data, "price")
filtered_data = filter_data(data, "color", "Голубой")
price_stats = calculate_statistics(data, "price")
category_frequencies = count_frequencies(data, "category")

print(f"\nТоп 5 товаров по цене:")
for item in sorted_data[:5]:
    print(f"ID: {item.get('id')}, Цена: {item.get('price')}, Название: {item.get('name')}")

print(f"\nТовары с цветом 'Голубой':")
for item in filtered_data:
    print(f"ID: {item.get('id')}, Цвет: {item.get('color')}, Название: {item.get('name')}")

print(f"\nСтатистика по цене:")
print(f"Общая сумма: {price_stats['sum']}")
print(f"Минимальная цена: {price_stats['min']}")
print(f"Максимальная цена: {price_stats['max']}")
print(f"Средняя цена: {price_stats['mean']:.2f}")

print(f"\nЧастота категорий товаров:")
for category, count in category_frequencies.items():
    print(f"{category}: {count} товаров")
