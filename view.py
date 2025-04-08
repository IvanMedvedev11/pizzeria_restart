from tkinter import *
from tkinter import ttk


class Authorization_Root:
    def __init__(self, root):
        self.root = root
        self.root.title("Пиццерия")
        self.root.geometry("500x500")

        # Инициализация переменных для хранения данных
        self.name_var = StringVar()
        self.last_name_var = StringVar()
        self.birthday_var = StringVar()

        self.Root_ui()


    def Root_ui(self):
        self.btn_Authorization = Button(self.root, text="Авторизация", command=self.Authorization)
        self.btn_Authorization.place(x=200, y=100)

    def Authorization(self):
        # Очищаем окно перед созданием новых элементов
        for widget in self.root.winfo_children():
            widget.destroy()

        username_label = Label(self.root, text="Username")
        username_label.place(x=160, y=200)
        self.name_entry = ttk.Entry(self.root, textvariable=self.name_var)
        self.name_entry.place(x=220, y=200)

        last_name_label = Label(self.root, text="Last name")
        last_name_label.place(x=160, y=230)
        self.last_name_entry = ttk.Entry(self.root, textvariable=self.last_name_var)
        self.last_name_entry.place(x=220, y=230)

        birthday_label = Label(self.root, text="Birthday")
        birthday_label.place(x=160, y=260)
        self.birthday_entry = ttk.Entry(self.root, textvariable=self.birthday_var)
        self.birthday_entry.place(x=220, y=260)

        self.btn_Confirm = Button(self.root, text="Подтвердить", command=self.Choice)
        self.btn_Confirm.place(x=230, y=290)

    def saved(self):
        # Получаем значения из переменных
        name = self.name_var.get()
        last_name = self.last_name_var.get()
        birthday = self.birthday_var.get()

        print(f"Имя: {name}, Фамилия: {last_name}, Дата рождения: {birthday}")
        return name, last_name, birthday

    def Choice(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.btn_pizza = Button(self.root, text="Выбрать готовую пицу", command=self.saved)
        self.btn_pizza.place(x=200, y=100)
        self.btn_ingredient = Button(self.root, text="Выбрать кастомную пицу", command=self.saved)
        self.btn_ingredient.place(x=200, y=200)


root = Tk()
app = Authorization_Root(root)
app.saved()
root.mainloop()

