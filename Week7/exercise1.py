import sqlite3

import time

class UserService:


     def get_user(self, user_id):
         conn = sqlite3.connect('app.db') # New connection
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM users WHERE id = ?", (user_id, ))
         result = cursor. fetchone ()
         conn.close()
         return result

class OrderService:
     def get_orders(self, user_id):
         conn = sqlite3.connect('app.db') # Another new connection
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM orders WHERE user_id = ?", (user_id, ))
         result = cursor. fetchall()
         conn.close()


if __name__ == "__main__":
    user_id = 1
    user_service = UserService()
    order_service = OrderService()

    # Setup database with sample data if not present
    def setup_db():
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, name TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY, user_id INTEGER, item TEXT
        )''')
        # Insert sample user if not exists
        cursor.execute('SELECT COUNT(*) FROM users WHERE id = 1')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (1, 'Alice'))
        # Insert sample orders if not exists
        cursor.execute('SELECT COUNT(*) FROM orders WHERE user_id = 1')
        if cursor.fetchone()[0] == 0:
            cursor.executemany('INSERT INTO orders (user_id, item) VALUES (?, ?)', [
                (1, 'Book'), (1, 'Pen')
            ])
        conn.commit()
        conn.close()

    setup_db()

    start = time.time()
    user = user_service.get_user(user_id)
    orders = order_service.get_orders(user_id)
    end = time.time()

    print(f"User: {user}")
    print(f"Orders: {orders}")
    print(f"Processing time: {end - start:.6f} seconds")