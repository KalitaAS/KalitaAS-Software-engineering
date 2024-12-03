import json
from bs4 import BeautifulSoup

def hendle_file(path):
    with open(path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    products = soup.find_all("div", attrs={'class': 'product-item'})
    items = []

    for product in products:
      item = {}
      item['id'] = int(product. a['data-id'])
      item['link'] = product.find_all('a') [1]['href']
      item['img'] = product.img['src']
      item['title'] = product.span.get_text().strip()
      item['price'] = float(product.price.get_text().replace('₽', '').replace(" ", "").strip())
      item['bonus'] = int(product. strong.get_text()
            .replace("+ начислим", "")
            .replace(" бонусов", "")
            .strip()
            )

      properties = product.ul.find_all("li")
      for prop in properties:
          item[prop['type']] = prop.get_text().strip()

      items.append(item)
    return items

items = hendle_file("/content/2/1.html")

sorted_items = sorted(items, key=lambda x: x['price'])

filtered_items = [item for item in items if 'OLED' in item.get('matrix', '')]

prices = [item['price'] for item in items]
total_price = sum(prices)
min_price = min(prices)
max_price = max(prices)
avg_price = total_price / len(prices)

camera_tags = [item.get('camera', '') for item in items]
camera_frequency = dict(Counter(camera_tags))

print("Отсортированные по цене товары:")
for item in sorted_items:
    print(item['title'], item['price'])

print("\nОтфильтрованные товары с матрицей 'OLED':")
for item in filtered_items:
    print(item['title'])

print(f"\nСтатистика по ценам: сумма = {total_price}, мин = {min_price}, макс = {max_price}, среднее = {avg_price}")

print("\nЧастота текстовых меток по камере:")
for camera, count in camera_frequency.items():
    print(f"{camera}: {count}")
