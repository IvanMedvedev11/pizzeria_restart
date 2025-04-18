import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

from model import Pizza, Admin, User, FileManager


class PizzaController:
    def __init__(self, view):
        self.view = view
        self.current_pizza = None
        self.current_user = None
        self.db_manager = FileManager()
        self.user_manager = User()
        self.view.set_controller(self)
        self._init_db()

    def _init_db(self):
        # Инициализация базы данных с тестовыми данными
        try:
            # Добавляем тестовые ингредиенты
            self.db_manager.cursor.executemany('''
                INSERT OR IGNORE INTO Products (name, price, count)
                VALUES (?, ?, ?)
            ''', [
                ('Сыр', 50, 100),
                ('Кетчуп', 30, 100),
                ('Майонез', 30, 100),
                ('Сырный соус', 40, 100),
                ('Пепперони', 70, 100),
                ('Грибы', 60, 100),
                ('Помидоры', 40, 100),
                ('Оливки', 50, 100),
                ('Колбаса', 60, 100)
            ])

            # Добавляем тестовые пиццы
            self.db_manager.cursor.executemany('''
                INSERT OR IGNORE INTO Products (name, price, count)
                VALUES (?, ?, ?)
            ''', [
                ('Пепперони', 350, 100),
                ('Маргарита', 300, 100),
                ('Четыре сыра', 400, 100),
                ('Гавайская', 380, 100)
            ])

            # Добавляем взрослые товары
            self.db_manager.cursor.executemany('''
                INSERT OR IGNORE INTO Products_18 (name, price, count)
                VALUES (?, ?, ?)
            ''', [
                ('Пиво', 120, 100),
                ('Водка', 200, 100),
                ('Вино', 250, 100),
                ('Кальян', 500, 100),
                ('Сигареты', 150, 100)
            ])

            self.db_manager.connection.commit()
        except Exception as e:
            print(f"Ошибка инициализации БД: {e}")

    def authenticate_user(self, name: str, last_name: str, birthday: str) -> bool:
        try:
            # Проверяем формат даты
            day, month, year = map(int, birthday.split('-'))
            birth_date = datetime(year=year, month=month, day=day)

            # Рассчитываем возраст
            today = datetime.now()
            age = today.year - birth_date.year
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1

            # Сохраняем пользователя
            result = self.user_manager.add_user(name, last_name, birthday, "123")  # номер временный
            if "успешно" not in result.lower():
                self.view.show_error(result)
                return False

            self.current_user = {
                'name': name,
                'last_name': last_name,
                'birthday': birthday,
                'is_adult': age >= 18
            }

            self.view.on_auth_success(self.current_user['is_adult'])
            return True

        except ValueError:
            self.view.show_error("Неверный формат даты. Используйте ДД-ММ-ГГГГ")
            return False
        except Exception as e:
            self.view.show_error(f"Ошибка аутентификации: {str(e)}")
            return False

    def get_pizza_list(self) -> List[Dict]:
        try:
            self.db_manager.cursor.execute('''
                SELECT name, price FROM Products 
                WHERE name IN ('Пепперони', 'Маргарита', 'Четыре сыра', 'Гавайская')
            ''')
            return [{'name': row[0], 'price': row[1]} for row in self.db_manager.cursor.fetchall()]
        except Exception as e:
            self.view.show_error(f"Ошибка загрузки меню: {str(e)}")
            return []

    def get_ingredients_list(self) -> List[Dict]:
        try:
            self.db_manager.cursor.execute('''
                SELECT name, price FROM Products 
                WHERE name NOT IN ('Пепперони', 'Маргарита', 'Четыре сыра', 'Гавайская')
            ''')
            return [{'name': row[0], 'price': row[1]} for row in self.db_manager.cursor.fetchall()]
        except Exception as e:
            self.view.show_error(f"Ошибка загрузки ингредиентов: {str(e)}")
            return []

    def get_adult_products_list(self) -> List[Dict]:
        try:
            self.db_manager.cursor.execute('SELECT name, price FROM Products_18')
            return [{'name': row[0], 'price': row[1]} for row in self.db_manager.cursor.fetchall()]
        except Exception as e:
            self.view.show_error(f"Ошибка загрузки взрослых товаров: {str(e)}")
            return []

    def create_custom_pizza(self, ingredients: Dict[str, int]) -> Optional[Dict]:
        try:
            pizza = Pizza("Кастомная пицца")
            total_price = 0

            for ingredient, quantity in ingredients.items():
                # Проверяем наличие ингредиента
                self.db_manager.cursor.execute(
                    'SELECT count, price FROM Products WHERE name = ?',
                    (ingredient,)
                )
                result = self.db_manager.cursor.fetchone()

                if not result or result[0] < quantity:
                    self.view.show_error(f"Недостаточно ингредиента: {ingredient}")
                    return None

                # Добавляем ингредиент в пиццу
                pizza.add_ingredient(ingredient, quantity, "Products")
                total_price += result[1] * quantity

            self.current_pizza = {
                'type': 'custom',
                'ingredients': ingredients,
                'price': total_price
            }

            return self.current_pizza

        except Exception as e:
            self.view.show_error(f"Ошибка создания пиццы: {str(e)}")
            return None

    def add_ready_pizza(self, pizza_name: str, size: str, quantity: int) -> Optional[Dict]:
        try:
            size_coefficients = {
                'Маленькая': 0.8,
                'Средняя': 1.0,
                'Большая': 1.2
            }

            self.db_manager.cursor.execute(
                'SELECT price FROM Products WHERE name = ?',
                (pizza_name,)
            )
            base_price = self.db_manager.cursor.fetchone()[0]

            # Рассчитываем итоговую цену
            total_price = base_price * size_coefficients.get(size, 1.0) * quantity

            self.current_pizza = {
                'type': 'ready',
                'name': pizza_name,
                'size': size,
                'quantity': quantity,
                'price': total_price
            }

            return self.current_pizza

        except Exception as e:
            self.view.show_error(f"Ошибка добавления пиццы: {str(e)}")
            return None

    def add_adult_product(self, product_name: str, quantity: int) -> Optional[Dict]:
        try:
            if not self.current_user or not self.current_user['is_adult']:
                self.view.show_error("Подтвердите возраст для заказа этих товаров")
                return None

            # Проверяем наличие товара
            self.db_manager.cursor.execute(
                'SELECT count, price FROM Products_18 WHERE name = ?',
                (product_name,)
            )
            result = self.db_manager.cursor.fetchone()

            if not result or result[0] < quantity:
                self.view.show_error(f"Недостаточно товара: {product_name}")
                return None

            total_price = result[1] * quantity

            adult_order = {
                'name': product_name,
                'quantity': quantity,
                'price': total_price
            }

            if not hasattr(self, 'adult_products'):
                self.adult_products = []

            self.adult_products.append(adult_order)
            return adult_order

        except Exception as e:
            self.view.show_error(f"Ошибка добавления товара: {str(e)}")
            return None

    def finalize_order(self) -> bool:
        try:
            if not self.current_user:
                self.view.show_error("Сначала авторизуйтесь")
                return False

            order_data = {
                'user': self.current_user,
                'pizza': self.current_pizza if hasattr(self, 'current_pizza') else None,
                'adult_products': self.adult_products if hasattr(self, 'adult_products') else None
            }


            self.view.on_order_success(order_data)

            if hasattr(self, 'current_pizza'):
                del self.current_pizza
            if hasattr(self, 'adult_products'):
                del self.adult_products

            return True

        except Exception as e:
            self.view.show_error(f"Ошибка оформления заказа: {str(e)}")
            return False

    def admin_login(self, password: str) -> bool:
        admin = Admin()
        result = admin.sign_in(password)
        if "успешно" in result.lower():
            self.view.show_admin_panel()
            return True
        self.view.show_error(result)
        return False

    def admin_update_product(self, product_type: str, product_name: str, field: str, new_value: str) -> bool:
        try:
            admin = Admin()
            table_name = "Products_18" if product_type == "adult" else "Products"

            if field == "price":
                new_value = int(new_value)
            elif field == "count":
                new_value = int(new_value)

            result = admin.change_ingredient(product_name, field, new_value, table_name)

            if "успешно" not in result.lower():
                self.view.show_error(result)
                return False

            self.view.show_success(f"Товар {product_name} успешно обновлен")
            return True

        except ValueError:
            self.view.show_error("Неверный формат числа")
            return False
        except Exception as e:
            self.view.show_error(f"Ошибка обновления: {str(e)}")
            return False
