import sqlite3
import pickle

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
            if item:
                items.append(item)
    return items


def load_pkl_file(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def create_tables(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            author TEXT,
            genre TEXT,
            pages INTEGER,
            published_year INTEGER,
            isbn TEXT,
            rating REAL,
            views INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subitems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            price INTEGER,
            place TEXT,
            date TEXT
        )
    """)
    db.commit()

# Функция для вставки данных
def insert_data(db, items, subitems):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO items (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES (:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views)
    """, items)
    cursor.executemany("""
        INSERT OR IGNORE INTO subitems (title, price, place, date)
        VALUES (:title, :price, :place, :date)
    """, subitems)
    db.commit()

def query_joined_data(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT items.title, items.author, subitems.price, subitems.place, subitems.date
        FROM items
        JOIN subitems ON items.title = subitems.title
        LIMIT 18

    """)
    for row in res.fetchall():
        print(f"Книга: {row[0]}, Автор: {row[1]}, Цена: {row[2]}, Место продажи: {row[3]}, Дата: {row[4]}")

def query_total_sales(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT subitems.title, SUM(subitems.price) as total_sales
        FROM subitems
        GROUP BY subitems.title
        ORDER BY total_sales DESC
    """)
    for row in res.fetchall():
        print(f"Книга: {row[0]}, Общая сумма продаж: {row[1]}")

def query_online_high_rating(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT DISTINCT items.title, items.author, items.rating, subitems.place
        FROM items
        JOIN subitems ON items.title = subitems.title
        WHERE subitems.place = 'online' AND items.rating > 4.6
    """)
    for row in res.fetchall():
        print(f"Книга: {row[0]}, Автор: {row[1]}, Рейтинг: {row[2]}, Место продажи: {row[3]}")

db = sqlite3.connect("books_and_sales.db")
create_tables(db)

items = load_text_file("item.text")
subitems = load_pkl_file("subitem.pkl")

insert_data(db, items, subitems)

print("Совместный вывод данных о книгах и продажах:")
query_joined_data(db)
print("\nОбщая сумма продаж для каждой книги:")
query_total_sales(db)
print("\nКниги, продававшиеся онлайн, с рейтингом выше 4.6:")
query_online_high_rating(db)
