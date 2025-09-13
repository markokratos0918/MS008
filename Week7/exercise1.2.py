import sqlite3

import time




# Singleton for database connection
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect('app.db')
        return cls._instance

    def get_connection(self):
        return self.conn



# Service to get user info from the database
class UserService:
    def get_user(self, user_id):
        # Use the singleton database connection
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id, ))
        result = cursor.fetchone()
        return result



# Service to get orders for a user
class OrderService:
    def get_orders(self, user_id):
        # Use the singleton database connection
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = ?", (user_id, ))
        result = cursor.fetchall()
        return result


if __name__ == "__main__":
    user_id = 1
    user_service = UserService()
    order_service = OrderService()

    # Setup database with sample data if not present

    # Function to set up the database and add sample data
    def setup_db():
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()
        # Create tables if they don't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, name TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY, user_id INTEGER, item TEXT
        )''')
        # Insert a sample user if not exists
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

    setup_db()

    start = time.time()
    user = user_service.get_user(user_id)
    orders = order_service.get_orders(user_id)
    end = time.time()

    print(f"User: {user}")
    print(f"Orders: {orders}")
    print(f"Processing time: {end - start:.6f} seconds")

    # Close the singleton connection at the end
    DatabaseConnection().get_connection().close()
