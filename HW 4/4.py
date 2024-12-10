import sqlite3
import pickle


def create_database():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        price REAL,
        quantity INTEGER,
        category TEXT,
        fromCity TEXT,
        isAvailable BOOLEAN,
        views INTEGER,
        updateCount INTEGER DEFAULT 0
    );''')
    conn.commit()
    return conn, cursor


def load_pickled_data():
    with open('_product_data.pkl', 'rb') as f:
        return pickle.load(f)


def insert_initial_data(cursor, data):
    for product in data:
        cursor.execute('''
        INSERT OR IGNORE INTO products 
        (name, price, quantity, category, fromCity, isAvailable, views) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
        ''', (
            product.get('name', None), 
            product.get('price', 0.0), 
            product.get('quantity', 0), 
            product.get('category', 'Unknown'), 
            product.get('fromCity', 'Unknown'), 
            product.get('isAvailable', False), 
            product.get('views', 0)
        ))


def process_update(cursor, name, method, param):
    cursor.execute('SELECT price, quantity, updateCount, isAvailable FROM products WHERE name = ?', (name,))
    result = cursor.fetchone()
    if not result:
        return False
    
    current_price, current_quantity, update_counter, is_available = result
    new_update_counter = update_counter + 1
    if method == 'price_abs':
        new_price = float(param)
        if new_price < 0:
            return False

        cursor.execute(
            'UPDATE products SET price = ?, updateCount = ? WHERE name = ?',
            (new_price, new_update_counter, name)
        )
        
    elif method == 'price_percent':
        change = float(param)
        new_price = current_price * (1 + change)
        if new_price < 0:
            return False

        cursor.execute(
            'UPDATE products SET price = ?, updateCount = ? WHERE name = ?',
            (new_price, new_update_counter, name)
        )
        
    elif method == 'quantity_add':
        change = int(param)
        new_quantity = current_quantity + change
        if new_quantity < 0:
            return False

        cursor.execute(
            'UPDATE products SET quantity = ?, updateCount = ? WHERE name = ?',
            (new_quantity, new_update_counter, name)
        )
        
    elif method == 'quantity_sub':
        change = int(param)
        new_quantity = current_quantity - abs(change)
        if new_quantity < 0:
            return False

        cursor.execute(
            'UPDATE products SET quantity = ?, updateCount = ? WHERE name = ?',
            (new_quantity, new_update_counter, name)
        )
        
    elif method == 'remove':
        cursor.execute(
            'UPDATE products SET isAvailable = 0, updateCount = ? WHERE name = ?',
            (new_update_counter, name)
        )
        
    elif method == 'available':
        cursor.execute(
            'UPDATE products SET isAvailable = 1, updateCount = ? WHERE name = ?',
            (new_update_counter, name)
        )
        
    return True


def process_updates(conn, cursor):
    with open('_update_data.text', 'r') as f:
        current_update = {}
        for line in f:
            line = line.strip()
            if line == '=====':
                if current_update:
                    conn.execute('BEGIN TRANSACTION')
                    success = process_update(cursor, 
                                          current_update.get('name'),
                                          current_update.get('method'),
                                          current_update.get('param', ''))
                    if success:
                        conn.commit()
                    else:
                        conn.rollback()
                    current_update = {}
            elif line:
                key, value = line.split('::')
                current_update[key] = value


def run_analysis(cursor):
    print('\n10 Самых обновяемых продуктов')
    cursor.execute('''
        SELECT name, updateCount
        FROM products
        ORDER BY updateCount DESC
        LIMIT 10
    ''')
    for name, counter in cursor.fetchall():
        print(f'{name}: {counter} updates')


    print('\nАнализ цен товаров по категориям')
    cursor.execute('''
        SELECT 
            category,
            COUNT(*) as count,
            SUM(price) as total,
            MIN(price) as min_price,
            MAX(price) as max_price,
            AVG(price) as avg_price
        FROM products
        WHERE isAvailable = 1
        GROUP BY category
    ''')
    for row in cursor.fetchall():
        print(f'\nCategory: {row[0]}')
        print(f'Count: {row[1]}')
        print(f'Total Price: {row[2]}')
        print(f'Min Price: {row[3]}')
        print(f'Max Price: {row[4]}')
        print(f'Avg Price: {row[5]}')


    print('\nАнализ остатков товаров по категориям')
    cursor.execute('''
        SELECT 
            category,
            SUM(quantity) as total,
            MIN(quantity) as min_qty,
            MAX(quantity) as max_qty,
            AVG(quantity) as avg_qty
        FROM products
        WHERE isAvailable = 1
        GROUP BY category
    ''')
    for row in cursor.fetchall():
        print(f'\nCategory: {row[0]}')
        print(f'Total Quantity: {row[1]}')
        print(f'Min Quantity: {row[2]}')
        print(f'Max Quantity: {row[3]}')
        print(f'Avg Quantity: {row[4]:.2f}')


    print('\nРедкие, но частообновляемые товары')
    cursor.execute('''
        SELECT name, quantity, updateCount, price
        FROM products
        WHERE isAvailable = 1
            AND quantity < 10
            AND updateCount > 5
        ORDER BY updateCount DESC
    ''')
    for name, qty, updates, price in cursor.fetchall():
        print(f'{name}: {qty} in stock, {updates} updates, price: {price:.2f}')


conn, cursor = create_database()

initial_data = load_pickled_data()
insert_initial_data(cursor, initial_data)
conn.commit()

process_updates(conn, cursor)

run_analysis(cursor)