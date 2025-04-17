import sqlite3
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from model import Pizza, Admin
class PizzaController:
    def __init__(self, view):
        self.view = view
        self.current_pizza = None
        self.current_user = None
        self.admin = Admin()
        self.db_connection = self._init_db()
    def _init_db(self):
        try:
            conn = sqlite3.connect('pizzeria.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    name TEXT PRIMARY KEY,
                    leftovers INTEGER DEFAULT 100 NOT NULL,
                    cost INTEGER DEFAULT 100 NOT NULL,
                    is_18 BOOLEAN DEFAULT FALSE NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT DEFAULT '' NOT NULL,
                    last_name TEXT,
                    birthday TEXT,
                    is_adult BOOLEAN DEFAULT FALSE
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    pizza_type TEXT NOT NULL,
                    total_price REAL NOT NULL,
                    order_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_ingredients (
                    order_id INTEGER,
                    ingredient_name TEXT,
                    quantity INTEGER NOT NULL CHECK (quantity > 0),
                    PRIMARY KEY (order_id, ingredient_name),
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (ingredient_name) REFERENCES products(name)
                )
            ''')
            cursor.execute('''
                INSERT OR IGNORE INTO products (name, leftovers, cost, is_18)
                VALUES 
                    ('Сыр', 100, 50, 0),
                    ('Пепперони', 100, 70, 0),
                    ('Пиво', 100, 120, 1),
                    ('Водка', 100, 200, 1)
            ''')
            conn.commit()
            return conn
        except Exception as e:
            self.view.show_error(f"Ошибка инициализации БД: {str(e)}")
            return None

    def authenticate_user(self, name: str, last_name: str, birthday: str) -> bool:
        try:
            day, month, year = map(int, birthday.split('-'))
            birth_date = f"{year}-{month}-{day}"
            age = datetime.now().year - year

            is_adult = age >= 18
            if not is_adult:
                self.view.show_error("Вам должно быть больше 18 лет!")
                return False
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO users (name, last_name, birthday, is_adult)
                VALUES (?, ?, ?, ?)
            ''', (name, last_name, birth_date, is_adult))
            self.db_connection.commit()
            self.current_user = {
                'id': cursor.lastrowid,
                'name': name,
                'last_name': last_name,
                'is_adult': is_adult
            }
            return True

        except Exception as e:
            self.view.show_error(f"Ошибка аутентификации: {str(e)}")
            return False

    def create_pizza(self, pizza_type: str) -> bool:
        try:
            self.current_pizza = Pizza(pizza_type)
            return True
        except Exception as e:
            self.view.show_error(f"Ошибка создания пиццы: {str(e)}")
            return False

    def add_ingredient(self, ingredient_name: str, quantity: int) -> bool:
        if not self.current_pizza:
            self.view.show_error("Сначала создайте пиццу")
            return False
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                SELECT leftovers, cost, is_18 
                FROM products 
                WHERE name = ?
            ''', (ingredient_name,))
            result = cursor.fetchone()
            if not result:
                self.view.show_error("Ингредиент не найден")
                return False
            leftovers, cost, is_18 = result
            if is_18 and not self.current_user.get('is_adult', False):
                self.view.show_error("Этот ингредиент только для взрослых!")
                return False
            if quantity > leftovers:
                self.view.show_error("Недостаточно ингредиентов")
                return False
            self.current_pizza.add_ingredient(ingredient_name, quantity, "products")
            cursor.execute('''
                UPDATE products 
                SET leftovers = leftovers - ? 
                WHERE name = ?
            ''', (quantity, ingredient_name))
            self.db_connection.commit()
            if hasattr(self.view, 'update_pizza_info'):
                self.view.update_pizza_info(
                    self.current_pizza.name,
                    self.current_pizza.price,
                    self.current_pizza.ingredients
                )
            return True
        except Exception as e:
            self.db_connection.rollback()
            self.view.show_error(f"Ошибка добавления ингредиента: {str(e)}")
            return False
    def finalize_order(self) -> bool:
        if not self.current_pizza or not self.current_user:
            self.view.show_error("Нет активного заказа или пользователя")
            return False
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO orders (user_id, pizza_type, total_price)
                VALUES (?, ?, ?)
            ''', (self.current_user['id'], self.current_pizza.name, self.current_pizza.price))
            order_id = cursor.lastrowid
            for ing in self.current_pizza.ingredients:
                cursor.execute('''
                    INSERT INTO order_ingredients (order_id, ingredient_name, quantity)
                    VALUES (?, ?, ?)
                ''', (order_id, ing['name'], ing['quantity']))
            self.db_connection.commit()
            self.view.show_success("Заказ успешно сохранен!")
            return True
        except Exception as e:
            self.db_connection.rollback()
            self.view.show_error(f"Ошибка сохранения заказа: {str(e)}")
            return False
    def get_available_ingredients(self, include_adult=False) -> List[Dict]:
        try:
            cursor = self.db_connection.cursor()

            if include_adult:
                cursor.execute('''
                    SELECT name, leftovers, cost 
                    FROM products 
                    WHERE leftovers > 0
                ''')
            else:
                cursor.execute('''
                    SELECT name, leftovers, cost 
                    FROM products 
                    WHERE leftovers > 0 AND is_18 = 0
                ''')

            return [
                {'name': row[0], 'leftovers': row[1], 'cost': row[2]}
                for row in cursor.fetchall()
            ]

        except Exception as e:
            self.view.show_error(f"Ошибка загрузки ингредиентов: {str(e)}")
            return []

    def admin_login(self, password: str) -> bool:
        result = self.admin.sign_in(password)
        if "успешно" in result.lower():
            return True
        self.view.show_error(result)
        return False

    def admin_update_product(self, product_name: str, field: str, new_value: int) -> bool:
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(f'''
                UPDATE products 
                SET {field} = ? 
                WHERE name = ?
            ''', (new_value, product_name))
            self.db_connection.commit()
            return True

        except Exception as e:
            self.db_connection.rollback()
            self.view.show_error(f"Ошибка обновления: {str(e)}")
            return False

    def __del__(self):
        if hasattr(self, 'db_connection') and self.db_connection:
            self.db_connection.close()
