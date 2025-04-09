from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re


class Authorization_Root:
    def __init__(self, root):
        self.root = root
        self.root.title("Пиццерия")
        self.root.geometry("500x500")

        # Инициализация переменных для хранения данных
        self.name_var = StringVar()
        self.last_name_var = StringVar()
        self.birthday_var = StringVar()
        self.Chees_int = IntVar()
        # Регулярное выражение для проверки даты
        self.date_pattern = r'(?<!\d)(?:0?[1-9]|[12][0-9]|3[01])-(?:0?[1-9]|1[0-2])-(?:19[0-9][0-9]|20[01][0-9])(?!\d)'

        self.Root_ui()

    def Root_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.btn_Authorization = Button(self.root, text="Авторизация", command=self.Authorization)
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

        self.btn_Confirm = Button(self.root, text="Подтвердить", command=self.validate_and_continue)
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
        name = self.name_var.get()
        last_name = self.last_name_var.get()
        birthday = self.birthday_var.get()

        print(f"Имя: {name}, Фамилия: {last_name}, Дата рождения: {birthday}")
        return name, last_name, birthday

    def Choice(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Выберите тип пиццы:").place(x=200, y=50)

        self.btn_pizza = Button(self.root, text="Готовая пицца", command=self.Pizza_choice)
        self.btn_pizza.place(x=200, y=100)

        self.btn_ingredient = Button(self.root, text="Кастомная пицца", command=self.Ingredient_choice)
        self.btn_ingredient.place(x=200, y=150)

    def Pizza_choice(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Выберите готовую пиццу:").place(x=200, y=50)

    def Ingredient_choice(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Label(self.root, text="Выберите инградиенты:").place(x=200, y=50)
        Label(self.root, text="Сыр").place(x=100, y=100)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=100)

        Label(self.root, text="Кетчуп").place(x=100, y=150)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=150)

        Label(self.root, text="майонез").place(x=100, y=200)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=200)

        Label(self.root, text="Сырный соус").place(x=100, y=250)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=250)

        Label(self.root, text="Пепперони").place(x=100, y=300)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=300)

        Label(self.root, text="Грибы").place(x=100, y=350)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=350)

        Label(self.root, text="Помидоры").place(x=100, y=400)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=400)

        Label(self.root, text="Оливки").place(x=100, y=450)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=450)

        Label(self.root, text="Колбаса").place(x=100, y=470)
        self.Chees_Entry = ttk.Entry(self.root, textvariable=self.Chees_int)
        self.Chees_Entry.place(x=200, y=470)

root = Tk()
app = Authorization_Root(root)
root.mainloop()

