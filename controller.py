import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from model import Pizza, Admin


class PizzaController:
    def __init__(self, view):
        self.view = view
        self.current_pizza = None
        self.current_user = None
        self.db = self._init_db()
        self.view.set_controller(self)

    def _init_db(self):
        conn = sqlite3.connect('pizzeria.db')
        cursor = conn.cursor()

        # Создание таблиц
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                birthday TEXT NOT NULL,
                is_adult BOOLEAN NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                name TEXT PRIMARY KEY,
                leftovers INTEGER NOT NULL,
                cost INTEGER NOT NULL,
                is_18 BOOLEAN NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products_18plus (
                name TEXT PRIMARY KEY,
                leftovers INTEGER NOT NULL,
                cost INTEGER NOT NULL
            )
        ''')

        # Добавляем тестовые данные
        cursor.executemany('''
            INSERT OR IGNORE INTO products (name, leftovers, cost, is_18)
            VALUES (?, ?, ?, ?)
        ''', [
            ('Сыр', 100, 50, 0),
            ('Кетчуп', 100, 30, 0),
            ('Пепперони', 100, 70, 0)
        ])

        cursor.executemany('''
            INSERT OR IGNORE INTO products_18plus (name, leftovers, cost)
            VALUES (?, ?, ?)
        ''', [
            ('Пиво', 100, 120),
            ('Водка', 100, 200)
        ])

        conn.commit()
        return conn

    def authenticate_user(self, name: str, last_name: str, birthday: str) -> bool:
        try:
            day, month, year = map(int, birthday.split('-'))
            age = datetime.now().year - year
            is_adult = age >= 18

            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO users (name, last_name, birthday, is_adult)
                VALUES (?, ?, ?, ?)
            ''', (name, last_name, birthday, is_adult))

            self.db.commit()
            self.current_user = {
                'id': cursor.lastrowid,
                'name': name,
                'is_adult': is_adult
            }
            self.view.on_auth_success(is_adult)
            return True

        except Exception as e:
            self.view.show_error(f"Ошибка аутентификации: {str(e)}")
            return False

    def create_pizza(self, pizza_type: str) -> bool:
        try:
            self.current_pizza = Pizza(pizza_type)
            self.view.update_pizza_display(pizza_type, 0, [])
            return True
        except Exception as e:
            self.view.show_error(f"Ошибка создания пиццы: {str(e)}")
            return False

    def add_ingredient(self, ingredient_name: str, quantity: int) -> bool:
        if not self.current_pizza:
            self.view.show_error("Сначала создайте пиццу")
            return False

        try:
            table_name = "products_18plus" if ingredient_name in ["Пиво", "Водка"] else "products"
            result = self.current_pizza.add_ingredient(ingredient_name, quantity, table_name)

            if isinstance(result, str):
                self.view.show_error(result)
                return False

            self.view.update_pizza_display(
                self.current_pizza.name,
                self.current_pizza.price,
                self._get_current_ingredients()
            )

            return True

        except Exception as e:
            self.view.show_error(f"Ошибка добавления ингредиента: {str(e)}")
            return False

    def finalize_order(self) -> bool:
        if not self.current_pizza or not self.current_user:
            self.view.show_error("Нет активного заказа")
            return False

        try:
            order_data = {
                'user': {
                    'name': self.current_user['name'],
                    'is_adult': self.current_user['is_adult']
                },
                'pizza': {
                    'type': self.current_pizza.name,
                    'price': self.current_pizza.price,
                    'ingredients': self._get_current_ingredients()
                }
            }

            self.view.on_order_success(order_data)
            self.current_pizza = None
            return True

        except Exception as e:
            self.view.show_error(f"Ошибка сохранения заказа: {str(e)}")
            return False

    def get_available_ingredients(self, include_adult=False) -> List[Dict]:
        try:
            cursor = self.db.cursor()

            if include_adult:
                cursor.execute('''
                    SELECT name, leftovers, cost 
                    FROM products
                    UNION ALL
                    SELECT name, leftovers, cost 
                    FROM products_18plus
                    WHERE leftovers > 0
                ''')
            else:
                cursor.execute('''
                    SELECT name, leftovers, cost 
                    FROM products 
                    WHERE leftovers > 0
                ''')

            return [{
                'name': row[0],
                'leftovers': row[1],
                'price': row[2]
            } for row in cursor.fetchall()]

        except Exception as e:
            self.view.show_error(f"Ошибка загрузки ингредиентов: {str(e)}")
            return []

    def _get_current_ingredients(self) -> List[Dict]:
        return []

    def admin_login(self, password: str) -> bool:
        admin = Admin()
        result = admin.sign_in(password)
        if "успешно" in result.lower():
            self.view.show_admin_panel()
            return True
        self.view.show_error(result)
        return False

    def admin_update_product(self, product_name: str, field: str, new_value: int) -> bool:
        try:
            admin = Admin()
            table_name = "products_18plus" if product_name in ["Пиво", "Водка"] else "products"
            result = admin.change_ingredient(product_name, field, new_value, table_name)

            if "успешно" not in result.lower():
                self.view.show_error(result)
                return False

            self.view.show_success(result)
            return True

        except Exception as e:
            self.view.show_error(f"Ошибка обновления: {str(e)}")
            return False
