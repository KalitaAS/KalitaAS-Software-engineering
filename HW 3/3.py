import os
import json
from bs4 import BeautifulSoup
from collections import Counter

def handle_file(path):
    with open(path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    soup = BeautifulSoup(xml_content, "xml")
    star_data = {}

    star_data["name"] = soup.find("name").get_text().strip()
    star_data["constellation"] = soup.find("constellation").get_text().strip()
    star_data["spectral_class"] = soup.find("spectral-class").get_text().strip()
    star_data["radius"] = float(soup.find("radius").get_text().strip())
    star_data["rotation"] = float(soup.find("rotation").get_text().replace("days", "").strip())
    star_data["age"] = float(soup.find("age").get_text().replace("billion years", "").strip())
    star_data["distance"] = float(soup.find("distance").get_text().replace("million km", "").strip())
    star_data["absolute_magnitude"] = float(soup.find("absolute-magnitude").get_text().replace("million km", "").strip())
    return star_data

def parse_all_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory, filename)
            all_data.append(handle_file(file_path))
    return all_data

def analyze_data(data):
    sorted_data = sorted(data, key=lambda x: x['radius'])

    filtered_data = [star for star in data if star['constellation'] == "Скорпион"]

    distances = [star['distance'] for star in data]
    total_distance = sum(distances)
    min_distance = min(distances)
    max_distance = max(distances)
    avg_distance = total_distance / len(distances)

    spectral_classes = [star['spectral_class'] for star in data]
    spectral_frequency = dict(Counter(spectral_classes))

    return {
        "sorted_data": sorted_data,
        "filtered_data": filtered_data,
        "statistics": {
            "total_distance": total_distance,
            "min_distance": min_distance,
            "max_distance": max_distance,
            "avg_distance": avg_distance
        },
        "spectral_frequency": spectral_frequency
    }

directory_path = "/content/3"
parsed_data = parse_all_files(directory_path)

with open("parsed_data.json", "w", encoding="utf-8") as json_file:
    json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)

analysis_results = analyze_data(parsed_data)

print("Сортировка по радиусу:")
for star in analysis_results["sorted_data"][:10]:
    print(star)

print("\nФильтрованные данные (Скорпион):")
for star in analysis_results["filtered_data"]:
    print(star)

print("\nСтатистика для расстояния:")
print(analysis_results["statistics"])

print("\nЧастота спектральных классов:")
for spectral_class, count in analysis_results["spectral_frequency"].items():
    print(f"{spectral_class}: {count}")
