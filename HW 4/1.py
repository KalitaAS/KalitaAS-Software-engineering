import sqlite3
import json

def load_text_file(filename):
    items = []
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        entries = content.strip().split("=====\n")
        for entry in entries:
            item = {}
            for line in entry.splitlines():
                if "::" in line:  
                    key, value = line.split("::", 1) 
                    key = key.strip()
                    value = value.strip()
                    if key in ["pages", "published_year", "rating", "views"]:
                        value = float(value) if "." in value else int(value)
                    item[key] = value
                items.append(item)
    return items


def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            pages INTEGER,
            published_year INTEGER,
            isbn TEXT,
            rating REAL,
            views INTEGER
        )
    """)
    db.commit()

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO books (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES (:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views)
    """, items)
    db.commit()

def query_first_sorted(db, output_file):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * FROM books
        ORDER BY views DESC
        LIMIT 18
    """)
    rows = [dict(zip([column[0] for column in cursor.description], row)) for row in res.fetchall()]
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=4)

def query_numeric_stats(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT SUM(views), MIN(views), MAX(views), AVG(views)
        FROM books
    """)
    stats = res.fetchone()
    print(f"Сумма просмотров: {stats[0]}, Минимум: {stats[1]}, Максимум: {stats[2]}, Среднее: {stats[3]}")

def query_category_frequency(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT genre, COUNT(*) as count
        FROM books
        GROUP BY genre
        ORDER BY count DESC
    """)
    for row in res.fetchall():
        print(f"Жанр: {row[0]}, Количество книг: {row[1]}")

def query_filtered_sorted(db, output_file):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * FROM books
        WHERE rating > 1.0
        ORDER BY views DESC
        LIMIT 18
    """)
    rows = [dict(zip([column[0] for column in cursor.description], row)) for row in res.fetchall()]
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=4)

db = sqlite3.connect("books_data.db")
create_table(db)
items = load_text_file("item.text")
insert_data(db, items)
query_first_sorted(db, "first_books.json")
print("Статистика по просмотрам")
query_numeric_stats(db)
print("\nЧастота встречаемости жанров")
query_category_frequency(db)
query_filtered_sorted(db, "filtered_books.json")
