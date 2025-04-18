
from tkinter import Tk
from view import Authorization_Root
from controller import PizzaController


def main():
    root = Tk()

    view = Authorization_Root(root)

    controller = PizzaController(view)

    root.mainloop()


if __name__ == "__main__":
    main()
