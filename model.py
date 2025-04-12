import hashlib
import sqlite3
class FileManager:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXIST Users (
        first_name TEXT IS NOT NULL
        last_name TEXT IS NOT NULL
        birthday DATETIME
        number TEXT IS NOT NULL
        )''')
        self.connection.commit()
        self.cursor.execute('''CREATE TABLE IF NOT EXIST Products (
                name TEXT IS NOT NULL
                price INTEGER
                count INTEGER
                )''')
        self.connection.commit()
        self.cursor.execute('''CREATE TABLE IF NOT EXIST Products_18+ (
                        name TEXT IS NOT NULL
                        price INTEGER
                        count INTEGER
                        )''')
        self.connection.commit()
class User:
    def __init__(self):
        self.databaser = FileManager()
    def add_user(self, first_name, last_name, birthday, number):
        self.databaser.cursor.execute('''SELECT * FROM Users WHERE number = ?''', (number))
        user = self.databaser.cursor.fetchone()
        if user is not None:
            return "Пользователь уже существует"
        self.databaser.cursor.execute('''INSERT INTO Users (first_name, last_name, birthday, number) VALUES (?, ?, ?, ?)''', (first_name, last_name, birthday, number))
        self.databaser.connection.commit()
        return "Вы успешно зарегистрированы"
class Pizza:
    def __init__(self, name):
        self.databaser = FileManager()
        self.name = name
        self.price = 0
    def add_ingredient(self, ingredient, count, table_name):
        self.databaser.cursor.execute('''SELECT count FROM ? WHERE name = ?''', (table_name, ingredient))
        product_count = self.databaser.cursor.fetchone()
        if product_count is None:
            return "Ингредиента не существует"
        product_count = product_count[0]
        if count > product_count:
            return "Не хватает ингредиентов"
        self.databaser.cursor.execute('''UPDATE ? SET count = count - ? WHERE name = ?''', (table_name, count, ingredient))
        self.databaser.connection.commit()
        self.databaser.cursor.execute('''SELECT price FROM ? WHERE name = ?''', (table_name, ingredient))
        price = self.databaser.cursor.fetchone()[0]
        self.price += price * count
    def add_size(self, size):
        size_coefficients = {"low": 0.8, "medium": 1, "high": 1.2}
        self.price *= size_coefficients[size]
class Admin:
    def __init__(self):
        self.hash_password = '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'
        self.state = False
    def sign_in(self, user_password):
        hash_user = hashlib.sha256(user_password.encode()).hexdigest()
        if hash_user == self.hash_password:
            self.state = True
            return "Вы успешно вошли"
        return "Неверный пароль"
    def change_ingredient(self, ingredient, stat, to_change, database):
        for i in range(len(database)):
            if database[i]['name'] == ingredient:
                database[i][stat] = to_change
                return "Данные успешно изменены"
