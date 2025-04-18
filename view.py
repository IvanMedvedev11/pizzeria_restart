from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
from datetime import datetime


class Authorization_Root:
    def __init__(self, root):
        self.root = root
        self.root.title("Пиццерия - Заказ онлайн")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#f5f5f5')

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.bg_color = '#f5f5f5'
        self.primary_color = '#ff6b6b'
        self.secondary_color = '#4ecdc4'
        self.accent_color = '#ffbe0b'
        self.text_color = '#333333'

        self.style.configure('TButton',
                             font=('Helvetica', 12),
                             padding=10,
                             background=self.primary_color,
                             foreground='white')
        self.style.map('TButton',
                       background=[('active', self.secondary_color)])

        self.style.configure('TLabel',
                             font=('Helvetica', 12),
                             background=self.bg_color,
                             foreground=self.text_color)

        self.style.configure('TEntry',
                             font=('Helvetica', 12),
                             padding=5)

        self.style.configure('TRadiobutton',
                             font=('Helvetica', 11),
                             background=self.bg_color,
                             foreground=self.text_color)



        self.name_var = StringVar()
        self.last_name_var = StringVar()
        self.birthday_var = StringVar()

        self.Chees_int = IntVar()
        self.Ketchup_int = IntVar()
        self.Mayonnaise_int = IntVar()
        self.Cheese_sauce_int = IntVar()
        self.Pepperoni_int = IntVar()
        self.Mushrooms_int = IntVar()
        self.Tomatoes_int = IntVar()
        self.Olives_int = IntVar()
        self.Sausage_int = IntVar()

        self.Beer_int = IntVar()
        self.Vodka_int = IntVar()
        self.Wine_int = IntVar()
        self.Hookah_int = IntVar()
        self.Cigarettes_int = IntVar()

        self.Pepperoni_pizza_int = IntVar()
        self.Margherita_int = IntVar()
        self.Four_Cheese_int = IntVar()
        self.Hawaiian_int = IntVar()

        self.pepperoni_size = StringVar(value='Средняя')
        self.margherita_size = StringVar(value='Средняя')
        self.four_cheese_size = StringVar(value='Средняя')
        self.hawaiian_size = StringVar(value='Средняя')

        self.date_pattern = r'(?<!\d)(?:0?[1-9]|[12][0-9]|3[01])-(?:0?[1-9]|1[0-2])-(?:19[0-9][0-9]|20[01][0-9])(?!\d)'

        self.Root_ui()

    def set_controller(self, controller):
        self.controller = controller

    def on_auth_success(self, is_adult):
        self.is_adult = is_adult
        self.Choice()

    def show_error(self, message):
        messagebox.showerror("Ошибка", message)

    def show_success(self, message):
        messagebox.showinfo("Успех", message)

    def show_admin_panel(self):
        pass
    def is_over_18(self):
        if not re.fullmatch(self.date_pattern, self.birthday_var.get()):
            return False


        day, month, year = map(int, self.birthday_var.get().split('-'))
        birth_date = datetime(year=year, month=month, day=day)
        today = datetime.now()

        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        if age >= 18:
            self.Adult_menu()
        else:
            messagebox.showerror("Ошибка", "Вам должно быть больше 18!")
    def Root_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.btn_Authorization = ttk.Button(self.root, text="Авторизация", command=self.Authorization, style='TButton')
        self.btn_Authorization.place(x=200, y=100)

    def Authorization(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Username").place(x=160, y=200)
        self.name_entry = ttk.Entry(self.root, textvariable=self.name_var)
        self.name_entry.place(x=220, y=200)

        Label(self.root, text="Last name").place(x=160, y=230)
        self.last_name_entry = ttk.Entry(self.root, textvariable=self.last_name_var)
        self.last_name_entry.place(x=220, y=230)

        Label(self.root, text="Birthday").place(x=160, y=260)
        self.birthday_entry = ttk.Entry(self.root, textvariable=self.birthday_var)
        self.birthday_entry.place(x=220, y=260)

        self.btn_Confirm = ttk.Button(self.root, text="Подтвердить", command=self.validate_and_continue, style='TButton')
        self.btn_Confirm.place(x=230, y=290)

    def validate_and_continue(self):

        if not all([self.name_var.get(), self.last_name_var.get(), self.birthday_var.get()]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        if not re.fullmatch(self.date_pattern, self.birthday_var.get()):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте дд-мм-гггг")
            return
        self.Choice()

    def saved(self):
        self.order_dict = {
            'user_info': {},
            'pizzas': {},
            'ingredients': {},
            'adult_items': {}
        }
        self.order_dict['user_info'] = {
            'name': self.name_var.get(),
            'last_name': self.last_name_var.get(),
            'birthday': self.birthday_var.get()
        }
        pizzas = {}
        if self.Pepperoni_pizza_int.get() > 0:
            pizzas['Пепперони'] = {
                'количество': self.Pepperoni_pizza_int.get(),
                'размер': self.pepperoni_size.get()
            }
        if self.Margherita_int.get() > 0:
            pizzas['Маргарита'] = {
                'количество': self.Margherita_int.get(),
                'размер': self.margherita_size.get()
            }
        if self.Four_Cheese_int.get() > 0:
            pizzas['Четыре сыра'] = {
                'количество': self.Four_Cheese_int.get(),
                'размер': self.four_cheese_size.get()
            }
        if self.Hawaiian_int.get() > 0:
            pizzas['Гавайская'] = {
                'количество': self.Hawaiian_int.get(),
                'размер': self.hawaiian_size.get()
            }
        self.order_dict['pizzas'] = pizzas

        ingredients = {}
        if self.Chees_int.get() > 0:
            ingredients['Сыр'] = self.Chees_int.get()
        if self.Ketchup_int.get() > 0:
            ingredients['Кетчуп'] = self.Ketchup_int.get()

        self.order_dict['ingredients'] = ingredients

        adult_items = {}
        if self.Beer_int.get() > 0:
            adult_items['Пиво'] = self.Beer_int.get()\

        self.order_dict['adult_items'] = adult_items

        print("Полный заказ:")
        print(self.order_dict)

        messagebox.showinfo("Заказ сохранен", "Ваш заказ был сохранен!")
        self.Root_ui()

        return self.order_dict

        adult_items = {}
        if self.Beer_int.get() > 0:
            adult_items['Пиво'] = self.Beer_int.get()
        if self.Vodka_int.get() > 0:
            adult_items['Водка'] = self.Vodka_int.get()
        if self.Wine_int.get() > 0:
            adult_items['Вино'] = self.Wine_int.get()
        if self.Hookah_int.get() > 0:
            adult_items['Кальян'] = self.Hookah_int.get()
        if self.Cigarettes_int.get() > 0:
            adult_items['Сигареты'] = self.Cigarettes_int.get()
        self.order_dict['adult_items'] = adult_items

        # Выводим весь заказ
        print("Весь заказ:")
        print(self.order_dict)

        # Показываем сообщение с подтверждением
        messagebox.showinfo("Заказ сохранен", "Ваш заказ был сохранен в системе!")
        self.Root_ui()

        return self.order_dict

    def Choice(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Выберите тип пиццы:").place(x=200, y=50)

        self.btn_pizza = ttk.Button(self.root, text="Готовая пицца", command=self.Pizza_choice, style='TButton')
        self.btn_pizza.place(x=200, y=100)

        self.btn_ingredient = ttk.Button(self.root, text="Кастомная пицца", command=self.Ingredient_choice, style='TButton')
        self.btn_ingredient.place(x=200, y=150)
        self.btn_18 = ttk.Button(self.root, text="Взрослые приколюшки", command=self.is_over_18, style='TButton')
        self.btn_18.place(x=200, y=300)
        self.btn_return = ttk.Button(self.root, text="Завершить заказ", command=self.saved, style='TButton')
        self.btn_return.place(x=200, y=400)

    def Pizza_choice(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Выберите готовую пиццу:").place(x=200, y=50)

        # Пепперони
        Label(self.root, text="Пепперони").place(x=100, y=100)
        self.Pepperoni_pizza_Entry = ttk.Entry(self.root, textvariable=self.Pepperoni_pizza_int)
        self.Pepperoni_pizza_Entry.place(x=200, y=100)
        ttk.Radiobutton(self.root, text="Маленькая", variable=self.pepperoni_size, value="Маленькая").place(x=300,
                                                                                                            y=100)
        ttk.Radiobutton(self.root, text="Средняя", variable=self.pepperoni_size, value="Средняя").place(x=400, y=100)
        ttk.Radiobutton(self.root, text="Большая", variable=self.pepperoni_size, value="Большая").place(x=500, y=100)

        # Маргарита
        Label(self.root, text="Маргарита").place(x=100, y=150)
        self.Margherita_Entry = ttk.Entry(self.root, textvariable=self.Margherita_int)
        self.Margherita_Entry.place(x=200, y=150)
        ttk.Radiobutton(self.root, text="Маленькая", variable=self.margherita_size, value="Маленькая").place(x=300,
                                                                                                             y=150)
        ttk.Radiobutton(self.root, text="Средняя", variable=self.margherita_size, value="Средняя").place(x=400, y=150)
        ttk.Radiobutton(self.root, text="Большая", variable=self.margherita_size, value="Большая").place(x=500, y=150)

        # Четыре сыра
        Label(self.root, text="Четыре сыра").place(x=100, y=200)
        self.Four_Cheese_Entry = ttk.Entry(self.root, textvariable=self.Four_Cheese_int)
        self.Four_Cheese_Entry.place(x=200, y=200)
        ttk.Radiobutton(self.root, text="Маленькая", variable=self.four_cheese_size, value="Маленькая").place(x=300,
                                                                                                              y=200)
        ttk.Radiobutton(self.root, text="Средняя", variable=self.four_cheese_size, value="Средняя").place(x=400, y=200)
        ttk.Radiobutton(self.root, text="Большая", variable=self.four_cheese_size, value="Большая").place(x=500, y=200)

        # Гавайская
        Label(self.root, text="Гавайская").place(x=100, y=250)
        self.Hawaiian_Entry = ttk.Entry(self.root, textvariable=self.Hawaiian_int)
        self.Hawaiian_Entry.place(x=200, y=250)
        ttk.Radiobutton(self.root, text="Маленькая", variable=self.hawaiian_size, value="Маленькая").place(x=300, y=250)
        ttk.Radiobutton(self.root, text="Средняя", variable=self.hawaiian_size, value="Средняя").place(x=400, y=250)
        ttk.Radiobutton(self.root, text="Большая", variable=self.hawaiian_size, value="Большая").place(x=500, y=250)

        self.btn_Confirm3 = ttk.Button(self.root, text="Подтвердить", command=self.Choice, style='TButton')
        self.btn_Confirm3.place(x=400, y=300)
    def Ingredient_choice(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Label(self.root, text="Выберите инградиенты:").place(x=200, y=50)
        Label(self.root, text="Сыр").place(x=100, y=100)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=100)

        Label(self.root, text="Кетчуп").place(x=100, y=150)
        self.Ketchup_Entry = ttk.Entry(self.root, textvariable=self.Ketchup_int)
        self.Ketchup_Entry.place(x=200, y=150)

        Label(self.root, text="майонез").place(x=100, y=200)
        self.Mayonnaise_Entry = ttk.Entry(self.root, textvariable=self.Mayonnaise_int)
        self.Mayonnaise_Entry.place(x=200, y=200)

        Label(self.root, text="Сырный соус").place(x=100, y=250)
        self.Cheese_sauce_Entry = ttk.Entry(self.root, textvariable=self.Cheese_sauce_int)
        self.Cheese_sauce_Entry.place(x=200, y=250)

        Label(self.root, text="Пепперони").place(x=100, y=300)
        self.Pepperoni_Entry = ttk.Entry(self.root, textvariable=self.Pepperoni_int)
        self.Pepperoni_Entry.place(x=200, y=300)

        Label(self.root, text="Грибы").place(x=100, y=350)
        self.Mushrooms_Entry = ttk.Entry(self.root, textvariable=self.Mushrooms_int)
        self.Mushrooms_Entry.place(x=200, y=350)

        Label(self.root, text="Помидоры").place(x=100, y=400)
        self.Tomatoes_Entry = ttk.Entry(self.root, textvariable=self.Tomatoes_int)
        self.Tomatoes_Entry.place(x=200, y=400)

        Label(self.root, text="Оливки").place(x=100, y=450)
        self.Olives_Entry = ttk.Entry(self.root, textvariable=self.Olives_int)
        self.Olives_Entry.place(x=200, y=450)

        Label(self.root, text="Колбаса").place(x=100, y=500)
        self.Sausage_Entry = ttk.Entry(self.root, textvariable=self.Sausage_int)
        self.Sausage_Entry.place(x=200, y=500)

        self.btn_Confirm1 = ttk.Button(self.root, text="Подтвердить", command= self.Choice, style='TButton')
        self.btn_Confirm1.place(x=400, y=250)
    def Adult_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Label(self.root, text="Выберите что то вредное):").place(x=200, y=50)
        Label(self.root, text="Пиво").place(x=100, y=100)
        self.Beer_Entry = ttk.Entry(self.root, textvariable=self.Beer_int)
        self.Beer_Entry.place(x=200, y=100)

        Label(self.root, text="Водка").place(x=100, y=150)
        self.Vodka_Entry = ttk.Entry(self.root, textvariable=self.Vodka_int)
        self.Vodka_Entry.place(x=200, y=150)

        Label(self.root, text="Вино").place(x=100, y=200)
        self.Wine_Entry = ttk.Entry(self.root, textvariable=self.Wine_int)
        self.Wine_Entry.place(x=200, y=200)

        Label(self.root, text="Кальянчик").place(x=100, y=250)
        self.Hookah_Entry = ttk.Entry(self.root, textvariable=self.Hookah_int)
        self.Hookah_Entry.place(x=200, y=250)

        Label(self.root, text="Сигареты").place(x=100, y=300)
        self.Cigarettes_Entry = ttk.Entry(self.root, textvariable=self.Cigarettes_int)
        self.Cigarettes_Entry.place(x=200, y=300)

        self.btn_Confirm2 = ttk.Button(self.root, text="Подтвердить", command= self.Choice, style='TButton')
        self.btn_Confirm2.place(x=400, y=250)
root = Tk()
app = Authorization_Root(root)
root.mainloop()
        self.btn_Confirm2 = ttk.Button(self.root, text="Подтвердить", command= self.Choice, style='TButton')
        self.btn_Confirm2.place(x=400, y=250)
root = Tk()
app = Authorization_Root(root)
root.mainloop()
