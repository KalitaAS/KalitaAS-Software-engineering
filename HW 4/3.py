import sqlite3
import json
import pickle

def load_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def load_pickle_file(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT,
            song TEXT,
            duration_ms INTEGER,
            year INTEGER,
            tempo REAL,
            genre TEXT,
            explicit BOOLEAN,
            popularity INTEGER,
            danceability REAL,
            acousticness REAL,
            energy REAL
        )
    """)
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    for entry in data:
        cursor.execute("""
            INSERT INTO songs (artist, song, duration_ms, year, tempo, genre, explicit, popularity, danceability, acousticness, energy)
            VALUES (:artist, :song, :duration_ms, :year, :tempo, :genre, :explicit, :popularity, :danceability, :acousticness, :energy)
        """, entry)
    db.commit()

def transform_data(json_data, pickle_data):
    result = []

    for entry in json_data:
        result.append({
            "artist": entry.get("artist"),
            "song": entry.get("song"),
            "duration_ms": int(entry.get("duration_ms")),
            "year": int(entry.get("year")),
            "tempo": float(entry.get("tempo")),
            "genre": entry.get("genre"),
            "explicit": entry.get("explicit") == "True",
            "popularity": int(entry.get("popularity")),
            "danceability": float(entry.get("danceability", 0)),
            "acousticness": None,
            "energy": None,
        })

    for entry in pickle_data:
        result.append({
            "artist": entry.get("artist"),
            "song": entry.get("song"),
            "duration_ms": int(entry.get("duration_ms")),
            "year": int(entry.get("year")),
            "tempo": float(entry.get("tempo")),
            "genre": entry.get("genre"),
            "explicit": False,  
            "popularity": int(entry.get("popularity")),
            "danceability": None,
            "acousticness": float(entry.get("acousticness", 0)),
            "energy": float(entry.get("energy", 0)),
        })

    return result

def export_to_json(db, filename):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * FROM songs
        ORDER BY popularity DESC
        LIMIT 18
    """).fetchall()

    rows = [
        {
            "id": row[0],
            "artist": row[1],
            "song": row[2],
            "duration_ms": row[3],
            "year": row[4],
            "tempo": row[5],
            "genre": row[6],
            "explicit": row[7],
            "popularity": row[8],
            "danceability": row[9],
            "acousticness": row[10],
            "energy": row[11],
        }
        for row in res
    ]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)

def calculate_statistics(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT SUM(popularity), MIN(popularity), MAX(popularity), AVG(popularity)
        FROM songs
    """).fetchone()
    print(f"Сумма: {res[0]}, Минимум: {res[1]}, Максимум: {res[2]}, Среднее: {res[3]:.2f}")

def genre_frequency(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT genre, COUNT(*) as count
        FROM songs
        GROUP BY genre
        ORDER BY count DESC
    """).fetchall()

    for row in res:
        print(f"Жанр: {row[0]}, Частота: {row[1]}")

def export_filtered_to_json(db, filename):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * FROM songs
        WHERE year > 2010
        ORDER BY popularity DESC
        LIMIT 23
    """).fetchall()

    rows = [
        {
            "id": row[0],
            "artist": row[1],
            "song": row[2],
            "duration_ms": row[3],
            "year": row[4],
            "tempo": row[5],
            "genre": row[6],
            "explicit": row[7],
            "popularity": row[8],
            "danceability": row[9],
            "acousticness": row[10],
            "energy": row[11],
        }
        for row in res
    ]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)

db = sqlite3.connect("songs.db")
create_table(db)

json_data = load_json_file("_part_1.json")
pickle_data = load_pickle_file("_part_2.pkl")

data = transform_data(json_data, pickle_data)
insert_data(db, data)

export_to_json(db, "songs.json")
print("Подсчёт суммы, минимума, максимума и среднего для popularity")
calculate_statistics(db)
print("\nЧастота встречаемости жанров")
genre_frequency(db)
export_filtered_to_json(db, "filtered_songs.json")
