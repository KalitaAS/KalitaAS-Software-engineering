import json
import os
from bs4 import BeautifulSoup
from collections import Counter

def extract_links_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]

    return links

all_links = []
for i in range(1, 41):
    file_path = os.path.join('/content', f'{i}.html')
    if os.path.exists(file_path):
        links = extract_links_from_html(file_path)
        all_links.extend(links)

with open('all_links.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_links, json_file, ensure_ascii=False, indent=4)

# Сортировка ссылок по алфавиту
sorted_links = sorted(all_links)

# Фильтрация по ссылкам, содержащим 'events'
filtered_links = [link for link in all_links if 'events' in link]

# Статистика по количеству ссылок
num_links = len(all_links)
average_links_per_file = num_links / 40  

# Частота слов
words_in_links = [link.split('/')[-1] for link in all_links if link]
word_freq = Counter(words_in_links)

with open('sorted_links.json', 'w', encoding='utf-8') as json_file:
    json.dump(sorted_links, json_file, ensure_ascii=False, indent=4)

with open('filtered_links.json', 'w', encoding='utf-8') as json_file:
    json.dump(filtered_links, json_file, ensure_ascii=False, indent=4)

# Статистика
statistics = {
    'total_links': num_links,
    'average_links_per_file': average_links_per_file
}

with open('statistics.json', 'w', encoding='utf-8') as json_file:
    json.dump(statistics, json_file, ensure_ascii=False, indent=4)


with open('word_frequency.json', 'w', encoding='utf-8') as json_file:
    json.dump(word_freq, json_file, ensure_ascii=False, indent=4)

