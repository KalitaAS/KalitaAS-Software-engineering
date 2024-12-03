import json
from bs4 import BeautifulSoup
from collections import Counter

def handle_file(path):
    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, features="html.parser")
    book_wrapper = soup.find("div", class_="book-wrapper")
    
    item = {}
    item['category'] = book_wrapper.find_all("span")[0].get_text().split(":")[1].strip()
    item['title'] = book_wrapper.find("h1", class_="book-title").get_text().strip()    
    item['author'] = book_wrapper.find("p", class_="author-p").get_text().strip()    
    pages = book_wrapper.find("span", class_="pages").get_text()
    item['pages'] = pages.split(":")[1].strip()
    year = book_wrapper.find("span", class_="year").get_text()
    item['year'] = year.split(":")[0].strip()
    isbn = book_wrapper.find_all("span")[2].get_text()  
    item['isbn'] = isbn.split(":")[0].strip()
    item['description'] = book_wrapper.find("p").get_text().strip()    
    rating_views = book_wrapper.find_all("span")[4:]  
    item['rating'] = float(rating_views[0].get_text().split(":")[1].strip())
    item['views'] = int(rating_views[1].get_text().split(":")[1].strip())
    item['img'] = book_wrapper.find("img")['src']
    
    return item

books = []
for i in range(2, 70):
    books.append(handle_file(f"./HW3 V8/1/{i}.html"))

with open('books.json', 'w', encoding='utf-8') as json_file:
    json.dump(books, json_file, ensure_ascii=False, indent=4)

# Сортировка по рейтингу
sorted_books_by_rating = sorted(books, key=lambda x: x['rating'], reverse=True)

# Фильтрация по просмотрам
filtered_books_by_views = [book for book in books if book['views'] > 50000]

with open('filtered_books_by_views.json', 'w', encoding='utf-8') as json_file:
    json.dump(filtered_books_by_views, json_file, ensure_ascii=False, indent=4)


views = [book['views'] for book in books]
views_sum = sum(views)
views_min = min(views)
views_max = max(views)
views_mean = sum(views) / len(views)

print(f"Сумма просмотров: {views_sum}")
print(f"Минимальное количество просмотров: {views_min}")
print(f"Максимальное количество просмотров: {views_max}")
print(f"Среднее количество просмотров: {views_mean}\n")

categories = [book['category'] for book in books]
category_counts = Counter(categories)

print("Частота категорий:")
for category, count in category_counts.items():
    print(f"{category}: {count}")
