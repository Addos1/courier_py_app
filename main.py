import tkinter as tk
import pyodbc
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tab_c import Example as TabC
from tab_b import Example as TabB

def Ok():
    uname = e1.get()
    password = e2.get()
    if(uname == "" and password == "") :
        messagebox.showinfo("", "Заполните имя пользователя и пароль")
 
 #вход удался и главное окно
    elif(uname == "Adel" and password == "123"):
        messagebox.showinfo("","Доступ открыт")
        master.destroy()
        class MainWindow(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent)

                self.parent = parent
                self.parent.title('Гостиница')

                self.init_ui()

            def init_ui(self):
                self.parent['padx'] = 10
                self.parent['pady'] = 10

                self.notebook = ttk.Notebook(self, width=400, height=500)

    
                b_tab = TabB(self.notebook)
                c_tab = TabC(self.notebook)

     
                self.notebook.add(b_tab, text="Регистрация")
                self.notebook.add(c_tab, text="Справочник")

                self.notebook.pack()

                self.pack()


        if __name__ == '__main__':
            root = Tk()
            root.title('Гостинница')
            ex = MainWindow(root)
            root.geometry("450x400")
            root.mainloop()
    else :
        messagebox.showinfo("","Неправильное имя пользователя или пароль")
 
 
master = Tk()
master.title("Логин")
master.geometry("300x200")
global e1
global e2
 
Label(master, text="Имя пользователя").place(x=10, y=10)
Label(master, text="Пароль").place(x=10, y=40)
 
e1 = Entry(master)
e1.place(x=140, y=10)

e2 = Entry(master)
e2.place(x=140, y=40)
e2.config(show="*")
 

Button(master, text="Войти", command=Ok ,height = 3, width = 13, bg="yellow").place(x=10, y=100)
