import json
import hashlib
class FileManager:
    def save_to_json(self, filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file)
    def save_to_txt(self, filename, data):
        with open(filename, 'w') as file:
            file.write(data)
    def load_json(self, filename):
        with open(filename, 'r') as file:
            json.load(file)
    def load_txt(self, filename):
        with open(filename, 'r') as file:
            file.read()
class Pizza:
    def __init__(self, name, database):
        self.name = name
        self.database = database
        self.price = 0
    def add_ingredient(self, ingredient, count):
        for elem in self.database:
            if elem['name'] == ingredient:
                if elem['count'] < count:
                    return "Не хватает ингредиентов"
                else:
                    elem['count'] -= count
                    index = self.database.index(elem)
                    self.database.pop(index)
                    self.database.insert(elem, index)
                ingredient_info = elem
                break
        else:
            return "Ингредиент не найден"
        self.price += ingredient_info['price'] * count
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

