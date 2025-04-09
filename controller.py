from model import FileManager, Pizza, Admin
import psycopg2
from typing import List, Dict, Union

class PizzaController:
    def __init__(self):
        self.file_manager = FileManager()
        self.admin = Admin()
        self.current_pizza = None
        self.database = self.load_ingredients()
        self.db_connection = self._connect_to_db()
    def _connect_to_db(self):
        try:
            return psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='1234',
                host='localhost'
            )
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            return None

    def load_ingredients(self) -> List[Dict]:
        if not self.db_connection:
            return []

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT name, leftovers, cost FROM products")
                return [
                    {'name': row[0], 'count': row[1], 'price': float(row[2])}
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            print(f"Ошибка загрузки ингредиентов: {e}")
            return []

    def create_pizza(self, pizza_type: str) -> Union[Pizza, str]:
        if not self.db_connection:
            return "Ошибка: Нет подключения к БД"

        self.current_pizza = Pizza(pizza_type, self.database)
        return self.current_pizza

    def add_ingredient_to_pizza(self, ingredient_name: str, count: int) -> str:
        if not self.current_pizza:
            return "Сначала создайте пиццу"

        result = self.current_pizza.add_ingredient(ingredient_name, count)
        if isinstance(result, str):
            return result
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE products SET leftovers = GREATEST(0, leftovers - %s) WHERE name = %s",
                    (count, ingredient_name)
                )
                self.db_connection.commit()
                for item in self.database:
                    if item['name'] == ingredient_name:
                        item['count'] -= count
                        break

            return "Ингредиент добавлен"
        except Exception as e:
            self.db_connection.rollback()
            return f"Ошибка обновления БД: {e}"

    def set_pizza_size(self, size: str) -> str:
        if not self.current_pizza:
            return "Сначала создайте пиццу"

        self.current_pizza.add_size(size)
        return f"Размер установлен. Текущая цена: {self.current_pizza.price}"

    def save_order(self, user_data: Dict) -> str:
        if not self.current_pizza:
            return "Нет активного заказа"
        json_order = {
            'user': user_data,
            'pizza': {
                'type': self.current_pizza.name,
                'price': self.current_pizza.price,
                'ingredients': [
                    {'name': ing, 'quantity': qty}
                    for ing, qty in self.current_pizza.ingredients
                ]
            }
        }
        self.file_manager.save_to_json('orders.json', json_order)

        if self.db_connection:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO orders (user_name, pizza_type, total_price) VALUES (%s, %s, %s) RETURNING id",
                        (user_data.get('name'), self.current_pizza.name, self.current_pizza.price)
                    )
                    order_id = cursor.fetchone()[0]

                    for ing, qty in self.current_pizza.ingredients:
                        cursor.execute(
                            "INSERT INTO order_ingredients (order_id, ingredient_name, quantity) VALUES (%s, %s, %s)",
                            (order_id, ing, qty)
                        )

                    self.db_connection.commit()

            except Exception as e:
                self.db_connection.rollback()
                return f"Заказ сохранен в JSON, но ошибка БД: {e}"

        return "Заказ сохранен в JSON и БД"

    def admin_change_ingredient(self, ingredient: str, stat: str, to_change: Union[int, float]) -> str:
        if not self.admin.state:
            return "Требуется авторизация"
        result = self.admin.change_ingredient(ingredient, stat, to_change, self.database)
        if not result.startswith("Данные успешно изменены"):
            return result
        if self.db_connection:
            try:
                with self.db_connection.cursor() as cursor:
                    if stat == 'count':
                        cursor.execute(
                            "UPDATE products SET leftovers = %s WHERE name = %s",
                            (to_change, ingredient)
                        )
                    elif stat == 'price':
                        cursor.execute(
                            "UPDATE products SET cost = %s WHERE name = %s",
                            (to_change, ingredient)
                        )
                    self.db_connection.commit()
                    return f"{result} (БД обновлена)"
            except Exception as e:
                self.db_connection.rollback()
                return f"{result} (Ошибка обновления БД: {e})"

        return f"{result} (БД не обновлена - нет подключения)"

    def get_available_ingredients(self) -> List[Dict]:
        return [{'name': item['name'], 'count': item['count']} for item in self.database if item['count'] > 0]

    def __del__(self):
        if hasattr(self, 'db_connection') and self.db_connection:
            self.db_connection.close()
