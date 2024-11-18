import csv

def read_csv(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'product_id': int(row['product_id']),
                'name': row['name'],
                'price': float(row['price']),
                'quantity': int(row['quantity']),
                'category': row['category'],
                'description': row['description'],
                'production_date': row['production_date'],
                'expiration_date': row['expiration_date'],
                #'rating': float(row['rating']),
                'status': row['status'],
            })
    return data

data = read_csv("./HW1 V8/fourth_task.txt")

total_price = 0
max_quantity = data[0]['quantity']
min_quantity = data[0]['quantity']

filtered_data = []

for item in data:
    total_price += item['price']
    if max_quantity < item['quantity']:
        max_quantity = item['quantity']
    if min_quantity > item['quantity']:
        min_quantity = item['quantity']
    if item['quantity'] > 727:
        filtered_data.append(item)

avg_price = total_price / len(data)

with open("fourth_task_summary.txt", "w", encoding="utf-8") as f:
    f.write(f"Среднее по price: {avg_price:.2f}\n")
    f.write(f"Максимум quantity: {max_quantity}\n")
    f.write(f"Минимум  quantity: {min_quantity}\n")

with open("fourth_task_filtered.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=filtered_data[0].keys())
    writer.writeheader()
    for row in filtered_data:
        writer.writerow(row)
