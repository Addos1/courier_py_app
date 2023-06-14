import tkinter as tk
from tkinter import *
import pyodbc

from tkinter import ttk
class Example(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.button = tk.Button(self, text='Информация о клиенте', command=self.curier, width = 100,  bg="yellow")
        self.button.pack()
        self.button1 = tk.Button(self, text='Информация о администраторе', command=self.client, width = 100,bg="yellow")
        self.button1.pack()
        self.button1 = tk.Button(self, text='Информация о комнате', command=self.product, width = 100, bg="yellow")
        self.button1.pack()
        self.button2 = tk.Button(self, text='Информация о реестре', command=self.company, width = 100,bg="yellow")
        self.button2.pack() 
        self.pack()


        
    def curier(self):
        root1 = tk.Toplevel(self)
        root1.title('Клиенты')
        root1.geometry("350x400")

        # соединение с базой
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Kurs_aisha;'
                              'Trusted_Connection=yes;')
        # создать курсор
        c = conn.cursor()

       
        def show(listbox):
            conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Kurs_aisha;'
                              'Trusted_Connection=yes;')
            c = conn.cursor()
            c.execute("exec aisha @i=3, @FIO=0, @IIN=0, @birthday='12.04.1998' ,@telephon=0 ,@EMAIL=0, @ID=0 ")
            records = c.fetchall()
            listBox =ttk.Treeview(editor, columns=cols, show='headings')
            for i, (FIO , IIN , birthday , telephone , EMAIL ) in enumerate(records, start=1):
                listBox.insert("", "end", values=(FIO , IIN , birthday , telephon , EMAIL ))
            conn.close()
            root1.deiconify()

        def show2():
            root1.withdraw()

            global editor
            editor = Tk()
            editor.title('Клиенты')

            cols = ('№', 'ФИО', 'ИИН', 'Дата рождения', 'Телефон','Почта' )
            listBox = ttk.Treeview(editor, columns=cols, show='headings')
            for col in cols:
                listBox.heading(col, text=col)
                listBox.grid(row=1, column=0, columnspan=2)
            closeButton = tk.Button(editor, text="Закрыть", width=15, command=editor.destroy, bg="yellow").grid(row=6, column=1)
            show(listBox)
                
        # Создать функцию редактирования для обновления записи
        def update():
                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
                c = conn.cursor()

                record_id = delete_box.get()
                
                # Запрос базы данных
                storedProc = "exec curier_proc @i=4, @FIO=?, @IIN=?, @W_PHONE=? , @M_PHONE=? , @EMAIL=?, @ID=?"
                params=(FIO_editor.get(),IIN_editor.get(),  W_editor.get(), M_editor.get(), EMAIL_editor.get(), record_id)
                
                c.execute(storedProc, params)
                #зафиксировать изменения
                conn.commit()

                # остановить связь с базой данных
                conn.close()

                editor.destroy()
                root1.deiconify()
        def edit():
                root1.withdraw()
                global editor
                editor = Tk()
                editor.title('Обновить')

                editor.geometry("420x200")
                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
                c = conn.cursor()

                record_id = delete_box.get()
                # Запрос базы данных
                
                storedProc = "exec curier_proc @i=3, @FIO=0,@IIN=0,  @W_PHONE=0, @M_PHONE=0 , @EMAIL=0, @ID=?"
                params=(record_id)
                c.execute(storedProc, params)
                records = c.fetchall()
                
                #Создание глобальных переменных для имен текстовых полей
                global FIO_editor
                global IIN_editor
                global W_editor
                global M_editor
                global EMAIL_editor


                # Создать текстовые поля

                IIN_editor = Entry(editor, width=30)
                IIN_editor.grid(row=1, column=1)
                FIO_editor = Entry(editor, width=30)
                FIO_editor.grid(row=0, column=1)
                W_editor = Entry(editor, width=30)
                W_editor.grid(row=2, column=1)
                M_editor = Entry(editor, width=30)
                M_editor.grid(row=3, column=1)
                EMAIL_editor = Entry(editor, width=30)
                EMAIL_editor.grid(row=4, column=1)

                
                # Создание меток текстовых полей
                IIN_label = Label(editor, text="ИИН")
                IIN_label.grid(row=1, column=0)
                FIO_label = Label(editor, text="ФИО")
                FIO_label.grid(row=0, column=0)
                W_label = Label(editor, text="Рабочий телефон")
                W_label.grid(row=2, column=0)
                M_label = Label(editor, text="Мобильный телефон")
                M_label.grid(row=3, column=0)
                EMAIL_label = Label(editor, text="Почта")
                EMAIL_label.grid(row=4, column=0)

                # Цикл через результаты
                for record in records:
                        IIN_editor.insert(0, record[1])
                        FIO_editor.insert(0, record[0])
                        W_editor.insert(0, record[2])
                        M_editor.insert(0, record[3])
                        EMAIL_editor.insert(0, record[4])

                
                # Создать кнопку «Сохранить» для сохранения отредактированной записи
                edit_btn = Button(editor, text="Сохранить запись", command=update,bg="yellow" )
                edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

        # Создать функцию для удаления записи
        def delete():
                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
                c = conn.cursor()

                # Удалить запись
                
                storedProc = "exec curier_proc @i=2, @FIO=0, @IIN=0, @W_PHONE=0, @M_PHONE=0 , @EMAIL=0, @ID=?"
                params=(delete_box.get())
                
                c.execute(storedProc, params)

                delete_box.delete(0, END)

                
                conn.commit()
                conn.close()
        # Создать функцию отправки для базы данных
        def submit():

                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')

                c = conn.cursor()

                storedProc = "exec curier_proc @i=1, @FIO= ?, @IIN=? ,  @W_PHONE=? , @M_PHONE=? , @EMAIL=?, @ID=0"
                params=(FIO.get(), IIN.get(),W_PHONE.get(), M_PHONE.get(), EMAIL.get() )
                
                c.execute(storedProc, params)

                conn.commit()
                conn.close()

                # Очистить текстовые поля
                IIN.delete(0, END)
                FIO.delete(0, END)
                W_PHONE.delete(0, END)
                M_PHONE.delete(0, END)
                EMAIL.delete(0, END)
                
        # Создать текстовые поля
        IIN = Entry(root1, width=30)
        IIN.grid(row=1, column=1)
        FIO = Entry(root1, width=30)
        FIO.grid(row=0, column=1, padx=20, pady=(10, 0) )
        W_PHONE = Entry(root1, width=30)
        W_PHONE.grid(row=2, column=1)
        M_PHONE = Entry(root1, width=30)
        M_PHONE.grid(row=3, column=1)
        EMAIL = Entry(root1, width=30)
        EMAIL.grid(row=4, column=1)
        delete_box = Entry(root1, width=30)
        delete_box.grid(row=9, column=1, pady=5)

        # Создание меток текстовых полей
        IIN_label = Label(root1, text="ИИН")
        IIN_label.grid(row=1, column=0)
        FIO_label = Label(root1, text="ФИО")
        FIO_label.grid(row=0, column=0,pady=(10, 0) )
        W_PHONE_label = Label(root1, text="Рабочий телефон")
        W_PHONE_label.grid(row=2, column=0)
        M_PHONE_label = Label(root1, text="Мобильный телефон")
        M_PHONE_label.grid(row=3, column=0)
        EMAIL_label = Label(root1, text="Почта")
        EMAIL_label.grid(row=4, column=0)
        delete_box_label = Label(root1, text="Выберите ID")
        delete_box_label.grid(row=9, column=0, pady=5)

        # Создать кнопку добавления
        submit_btn = Button(root1, text="Добавить запись", command=submit, bg="yellow")
        submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        # Создать кнопку показать
        query_btn = Button(root1, text="Показать всех курьеров", command=show2, bg="yellow")
        query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=80)
        # Создать кнопку удаления
        delete_btn = Button(root1, text="Удалить запись", command=delete, bg="yellow")
        delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Создать кнопку обновления
        edit_btn = Button(root1, text="Изменить запись", command=edit, bg="yellow")
        edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=95)

        conn.commit()
        conn.close()


    def client(self):
        root2 = tk.Toplevel(self)
        root2.title('Клиент')
        root2.geometry("330x400")

        # соединение с базой
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
        # создать курсор
        c = conn.cursor()

        def show(listBox):
                conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')
                # создать курсор
                c =conn.cursor()
                c.execute("exec output @i=3 ")
                records = c.fetchall()
                print(records)
                for i, (ID_CLI, NAME , IIN, PHONE, EMAIL , ADRESS) in enumerate(records, start=1):
                    listBox.insert("", "end", values=(ID_CLI, NAME , IIN, PHONE, EMAIL , ADRESS ))
                conn.close()
                root2.deiconify()
                
        def show2():
                root2.withdraw()
                global editor
                editor = Tk()
                editor.title('Клиенты')

                cols = ('ID','Имя получателя', 'ИИН', 'Телефон','Почта', 'Адрес' )
                listBox =ttk.Treeview(editor, columns=cols, show='headings')
                for col in cols:
                            listBox.heading(col, text=col)    
                            listBox.grid(row=1, column=0, columnspan=2)
                closeButton = tk.Button(editor, text="Закрыть", width=15, command=editor.destroy, bg="yellow").grid(row=6, column=1)
                show(listBox)

        # Создать функцию редактирования для обновления записи
        def update():
                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
                c = conn.cursor()

                record_id = delete_box.get()
                
                # Запрос базы данных
                storedProc = "exec client_proc @i=4, @NAME=?, @IIN=?, @PHONE=?, @EMAIL=?, @ADRESS=?, @ID=?"
                params=(NAME_editor.get(), IIN_editor.get(), PHONE_editor.get(), EMAIL_editor.get(), ADRESS_editor.get(), record_id)
                
                c.execute(storedProc, params)
                #зафиксировать изменения
                conn.commit()

                # остановить связь с базой данных
                conn.close()

                editor.destroy()
                root2.deiconify()
        def edit():
                root2.withdraw()
                global editor
                editor = Tk()
                editor.title('Обновить')

                editor.geometry("420x170")
                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
                c = conn.cursor()

                record_id = delete_box.get()
                # Запрос базы данных
                
                storedProc = "exec client_proc @i=3,  @NAME=0, @IIN=0, @PHONE=0, @EMAIL=0 , @ADRESS=0, @ID=?"
                params=(record_id)
                c.execute(storedProc, params)
                records = c.fetchall()
                
                #Создание глобальных переменных для имен текстовых полей
                global NAME_editor
                global IIN_editor
                global PHONE_editor
                global EMAIL_editor
                global ADRESS_editor


                # Создать текстовые поля
                NAME_editor = Entry(editor, width=30)
                NAME_editor.grid(row=0, column=1)
                IIN_editor = Entry(editor, width=30)
                IIN_editor.grid(row=1, column=1)
                PHONE_editor = Entry(editor, width=30)
                PHONE_editor.grid(row=2, column=1)
                EMAIL_editor = Entry(editor, width=30)
                EMAIL_editor.grid(row=3, column=1)
                ADRESS_editor = Entry(editor, width=30)
                ADRESS_editor.grid(row=4, column=1)

                
                # Создание меток текстовых полей
                NAME_label = Label(editor, text="Имя получателя")
                NAME_label.grid(row=0, column=0)
                IIN_label = Label(editor, text="ИИН")
                IIN_label.grid(row=1, column=0)
                PHONE_label = Label(editor, text="Телефон")
                PHONE_label.grid(row=2, column=0)
                EMAIL_label = Label(editor, text="Почта")
                EMAIL_label.grid(row=3, column=0)
                ADRESS_label = Label(editor, text="Адрес")
                ADRESS_label.grid(row=4, column=0)

                # Цикл через результаты
                for record in records:
                        NAME_editor.insert(0, record[0])
                        IIN_editor.insert(0, record[1])
                        PHONE_editor.insert(0, record[2])
                        EMAIL_editor.insert(0, record[3])
                        ADRESS_editor.insert(0, record[4])

                
                # Создать кнопку «Сохранить» для сохранения отредактированной записи
                edit_btn = Button(editor, text="Сохранить запись", command=update, bg="yellow")
                edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

        # Создать функцию для удаления записи
        def delete():
                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
                c = conn.cursor()

                # Удалить запись
                
                storedProc = "exec client_proc @i=2, @NAME=0, @IIN=0, @PHONE=0, @EMAIL=0 , @ADRESS=0, @ID=?"
                params=(delete_box.get())
                
                c.execute(storedProc, params)

                delete_box.delete(0, END)

                
                conn.commit()
                conn.close()
        # Создать функцию отправки для базы данных
        def submit():

                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')

                c = conn.cursor()

                storedProc = "exec client_proc @i=1, @NAME=?, @IIN=?, @PHONE=?, @EMAIL=?, @ADRESS=?, @ID=0"
                params=(NAME.get(), IIN.get(), PHONE.get(), EMAIL.get(), ADRESS.get() )
                
                c.execute(storedProc, params)

                conn.commit()
                conn.close()

                # Очистить текстовые поля
                NAME.delete(0, END)
                IIN.delete(0, END)
                PHONE.delete(0, END)
                EMAIL.delete(0, END)
                ADRESS.delete(0, END)
                
                
        # Создать текстовые поля
        NAME = Entry(root2, width=30)
        NAME.grid(row=0, column=1)
        IIN = Entry(root2, width=30)
        IIN.grid(row=1, column=1)
        PHONE = Entry(root2, width=30)
        PHONE.grid(row=2, column=1)
        EMAIL = Entry(root2, width=30)
        EMAIL.grid(row=3, column=1)
        ADRESS = Entry(root2, width=30)
        ADRESS.grid(row=4, column=1)
        delete_box = Entry(root2, width=30)
        delete_box.grid(row=9, column=1, pady=5)

        # Создание меток текстовых полей
        NAME_label = Label(root2, text="Имя получателя")
        NAME_label.grid(row=0, column=0)
        IIN_label = Label(root2, text="ИИН")
        IIN_label.grid(row=1, column=0)
        PHONE_label = Label(root2, text="телефон")
        PHONE_label.grid(row=2, column=0)
        EMAIL_label = Label(root2, text="Почта")
        EMAIL_label.grid(row=3, column=0)
        ADRESS_label = Label(root2, text="Адрес")
        ADRESS_label.grid(row=4, column=0)
        delete_box_label = Label(root2, text="Выберите ID")
        delete_box_label.grid(row=9, column=0, pady=5)

        # Создать кнопку добавления
        submit_btn = Button(root2, text="Добавить запись", command=submit, bg="yellow")
        submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        # Создать кнопку показать
        query_btn = Button(root2, text="Показать всех клиентов", command=show2, bg="yellow")
        query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=80)
        # Создать кнопку удаления
        delete_btn = Button(root2, text="Удалить запись", command=delete, bg="yellow")
        delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Создать кнопку обновления
        edit_btn = Button(root2, text="Изменить запись", command=edit, bg="yellow")
        edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=95)

        conn.commit()
        conn.close()
        
    def product(self):
        root4 = tk.Toplevel(self)
        root4.title('Товар')
        root4.geometry("350x400")

                # соединение с базой
        conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')
                # создать курсор
        c = conn.cursor()
        def show(listBox):
                        conn = pyodbc.connect('Driver={SQL Server};'
                                              'Server=ADELDOS;'
                                              'Database=Courier_comp1;'
                                              'Trusted_Connection=yes;')
                        # создать курсор
                        c =conn.cursor()
                        c.execute("exec output @i=4 ")
                        records = c.fetchall()
                        print(records)
                        for i, (ID_PROD, NAME, PRICE, PROD_COD, FK_COM, PROD_W, fk_meas) in enumerate(records, start=1):
                            listBox.insert("", "end", values=(ID_PROD, NAME, PRICE, PROD_COD , FK_COM, PROD_W, fk_meas))
                        conn.close()

                        root4.deiconify()
        def show2():     
                        root4.withdraw()
                        global editor
                        editor = Tk()
                        editor.title('Клиенты')

                        cols = ('ID','Название продукта', 'Цена', 'Код продукта','Компания ID', 'Вес', 'Единица измерения')
                        listBox =ttk.Treeview(editor, columns=cols, show='headings')
                        for col in cols:
                                    listBox.heading(col, text=col)    
                                    listBox.grid(row=1, column=0, columnspan=2)
                        closeButton = tk.Button(editor, text="Закрыть", width=15, command=editor.destroy, bg="yellow").grid(row=7, column=1)
                        show(listBox)
        # Создать функцию редактирования для обновления записи
        def update():
                        conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')
                        c = conn.cursor()

                        record_id = delete_box.get()
                        
                        # Запрос базы данных
                        storedProc = "exec product_proc @i=4, @PROD_COD=?, @NAME=?, @PRICE=?, @FK_COM=?, @PROD_W=?, @FK_MEAS=?, @ID=?" # проблема с fk_meas, FK_COM не знаю как сразу показатьв вес и название компании  
                        params=(PROD_COD_editor.get(), NAME_editor.get(), PRICE_editor.get(), FK_COM_editor.get(), PROD_W_editor.get(),FK_MEAS_editor.get(),  record_id)
                        
                        c.execute(storedProc, params)
                        #зафиксировать изменения
                        conn.commit()

                        # остановить связь с базой данных
                        conn.close()

                        editor.destroy()
                        root4.deiconify()
        def edit():
                        root4.withdraw()
                        global editor
                        editor = Tk()
                        editor.title('Обновить')

                        editor.geometry("420x200")
                        conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')
                        c = conn.cursor()

                        record_id = delete_box.get()
                        # Запрос базы данных
                        
                        storedProc = "exec product_proc @i=3,  @PROD_COD=0, @NAME=0, @PRICE=0, @FK_COM=0, @PROD_W=0, @FK_MEAS=0, @ID=?"
                        params=(record_id)
                        c.execute(storedProc, params)
                        records = c.fetchall()
                        
                        #Создание глобальных переменных для имен текстовых полей
                        global PROD_COD_editor
                        global NAME_editor
                        global PRICE_editor
                        global FK_COM_editor
                        global PROD_W_editor
                        global FK_MEAS_editor


                        # Создать текстовые поля
                        PROD_COD_editor = Entry(editor, width=30)
                        PROD_COD_editor.grid(row=0, column=1)
                        NAME_editor = Entry(editor, width=30)
                        NAME_editor.grid(row=1, column=1,)
                        PRICE_editor = Entry(editor, width=30)
                        PRICE_editor.grid(row=2, column=1)
                        FK_COM_editor = Entry(editor, width=30)
                        FK_COM_editor.grid(row=3, column=1)
                        PROD_W_editor = Entry(editor, width=30)
                        PROD_W_editor.grid(row=4, column=1)
                        FK_MEAS_editor = Entry(editor, width=30)
                        FK_MEAS_editor.grid(row=5, column=1)
                        
                        # Создание меток текстовых полей
                        PROD_COD_label=Label(editor, text="Код продукта")
                        PROD_COD_label.grid(row=0, column=0)
                        NAME_label = Label(editor, text="Название продукта")
                        NAME_label.grid(row=1, column=0)
                        PRICE_label = Label(editor, text="Цена")
                        PRICE_label.grid(row=2, column=0)
                        FK_COM_label = Label(editor, text="Компания ID")
                        FK_COM_label.grid(row=3, column=0)
                        PROD_W_label = Label(editor, text="Вес")
                        PROD_W_label.grid(row=4, column=0)
                        FK_MEAS_label = Label(editor, text="Единица измерения")
                        FK_MEAS_label.grid(row=5, column=0)

                        # Цикл через результаты
                        for record in records:
                                PROD_COD_editor.insert(0, record[0])
                                NAME_editor.insert(0, record[1])
                                PRICE_editor.insert(0, record[2])
                                FK_COM_editor.insert(0, record[3])
                                PROD_W_editor.insert(0, record[4])
                                FK_MEAS_editor.insert(0, record[5])

                        
                        # Создать кнопку «Сохранить» для сохранения отредактированной записи
                        edit_btn = Button(editor, text="Сохранить запись", command=update, bg="yellow")
                        edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

                # Создать функцию для удаления записи
        def delete():
                        conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')
                        c = conn.cursor()

                        # Удалить запись
                        
                        storedProc = "exec product_proc @i=2, @PROD_COD=0, @NAME=0, @PRICE=0, @FK_COM=0, @PROD_W=0, @FK_MEAS=0, @ID=?"
                        params=(delete_box.get())
                        
                        c.execute(storedProc, params)

                        delete_box.delete(0, END)

                        
                        conn.commit()
                        conn.close()
                # Создать функцию отправки для базы данных
        def submit():

                        conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')

                        c = conn.cursor()

                        storedProc = "exec product_proc @i=1, @PROD_COD=?, @NAME=?, @PRICE=?, @FK_COM=?, @PROD_W=?, @FK_MEAS=?, @ID=0"
                        params=(PROD_COD.get(), NAME.get(), PRICE.get(), FK_COM.get(), PROD_W.get(), FK_MEAS.get() )
                        
                        c.execute(storedProc, params)

                        conn.commit()
                        conn.close()

                        # Очистить текстовые поля
                        PROD_COD.delete(0, END)
                        NAME.delete(0, END)
                        PRICE.delete(0, END)
                        FK_COM.delete(0, END)
                        PROD_W.delete(0, END)
                        FK_MEAS.delete(0, END)
                        
                
                # Создать текстовые поля
        PROD_COD = Entry(root4, width=30)
        PROD_COD.grid(row=0, column=1, padx=20, pady=(10, 0))
        NAME = Entry(root4, width=30)
        NAME.grid(row=1, column=1)
        PRICE = Entry(root4, width=30)
        PRICE.grid(row=2, column=1)
        FK_COM = Entry(root4, width=30)
        FK_COM.grid(row=3, column=1)
        PROD_W = Entry(root4, width=30)
        PROD_W.grid(row=4, column=1)
        FK_MEAS = Entry(root4, width=30)
        FK_MEAS.grid(row=5, column=1)
        delete_box = Entry(root4, width=30)
        delete_box.grid(row=9, column=1, pady=5)

                # Создание меток текстовых полей
        PROD_COD_label = Label(root4, text="Код продукта")
        PROD_COD_label.grid(row=0, column=0, pady=(10, 0))
        NAME_label = Label(root4, text="Название продукта")
        NAME_label.grid(row=1, column=0)
        PRICE_label = Label(root4, text="Цена")
        PRICE_label.grid(row=2, column=0)
        FK_COM_label = Label(root4, text="Компания ID")
        FK_COM_label.grid(row=3, column=0)
        PROD_W_label = Label(root4, text="Вес")
        PROD_W_label.grid(row=4, column=0)
        FK_MEAS_label = Label(root4, text="Единица измерения")
        FK_MEAS_label.grid(row=5, column=0)
        delete_box_label = Label(root4, text="Выберите ID")
        delete_box_label.grid(row=9, column=0, pady=5)

                # Создать кнопку добавления
        submit_btn = Button(root4, text="Добавить запись", command=submit, bg="yellow")
        submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
                # Создать кнопку показать
        query_btn = Button(root4, text="Показать все товары", command=show2, bg="yellow")
        query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=80)
                # Создать кнопку удаления
        delete_btn = Button(root4, text="Удалить запись", command=delete, bg="yellow")
        delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

                # Создать кнопку обновления
        edit_btn = Button(root4, text="Изменить запись", command=edit, bg="yellow")
        edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=95)

        conn.commit()
        conn.close()

    def company(self):
        root3 = tk.Toplevel(self)
        root3.title('Компания')
        root3.geometry("350x300")

        # соединение с базой
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
        # создать курсор
        c = conn.cursor()
        
        def show(listBox):
                conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')
                # создать курсор
                c =conn.cursor()
                c.execute("exec output @i=1")
                records = c.fetchall()
                print(records)
                for i, (id_com, Name, phone, adress) in enumerate(records, start=1):
                    listBox.insert("", "end", values=(id_com, Name, phone, adress))
                conn.close()

                root3.deiconify()
        def show2 ():      
                root3.withdraw()
                global editor
                editor = Tk()
                editor.title('Компании')

                cols = ('ID', 'Название компании', 'Телефон','Адрес')
                listBox =ttk.Treeview(editor, columns=cols, show='headings')
                for col in cols:
                    listBox.heading(col, text=col)    
                    listBox.grid(row=1, column=0, columnspan=2)
                closeButton = tk.Button(editor, text="Закрыть", width=15, command=editor.destroy, bg="yellow").grid(row=4, column=1)

                show(listBox)
        # Создать функцию редактирования для обновления записи
        def update():
                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
                c = conn.cursor()

                record_id = delete_box.get()
                
                # Запрос базы данных
                storedProc = "exec company_proc @i=4, @NAME=?,  @PHONE=?,  @ADRESS=?, @ID=?"
                params=(NAME_editor.get(),  PHONE_editor.get(), ADRESS_editor.get(), record_id)
                
                c.execute(storedProc, params)
                #зафиксировать изменения
                conn.commit()

                # остановить связь с базой данных
                conn.close()

                editor.destroy()
                root3.deiconify()
        def edit():
                root3.withdraw()
                global editor
                editor = Tk()
                editor.title('Обновить')

                editor.geometry("325x125")
                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
                c = conn.cursor()

                record_id = delete_box.get()
                # Запрос базы данных
                
                storedProc = "exec company_proc @i=3,  @NAME=0,  @PHONE=0, @ADRESS=0, @ID=?"
                params=(record_id)
                c.execute(storedProc, params)
                records = c.fetchall()
                
                #Создание глобальных переменных для имен текстовых полей
                global NAME_editor
                global PHONE_editor
                global ADRESS_editor


                # Создать текстовые поля
                NAME_editor = Entry(editor, width=30)
                NAME_editor.grid(row=0, column=1)
                PHONE_editor = Entry(editor, width=30)
                PHONE_editor.grid(row=1, column=1)
                ADRESS_editor = Entry(editor, width=30)
                ADRESS_editor.grid(row=2, column=1)
                
                # Создание меток текстовых полей
                NAME_label = Label(editor, text="Название компании")
                NAME_label.grid(row=0, column=0)
                PHONE_label = Label(editor, text="Телефон")
                PHONE_label.grid(row=1, column=0)
                ADRESS_label = Label(editor, text="Адрес")
                ADRESS_label.grid(row=2, column=0)

                # Цикл через результаты
                for record in records:
                        NAME_editor.insert(0, record[0])
                        PHONE_editor.insert(0, record[1])
                        ADRESS_editor.insert(0, record[2])

                
                # Создать кнопку «Сохранить» для сохранения отредактированной записи
                edit_btn = Button(editor, text="Сохранить запись", command=update,bg="yellow")
                edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

        # Создать функцию для удаления записи
        def delete():
                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')
                c = conn.cursor()

                # Удалить запись
                
                storedProc = "exec company_proc @i=2, @NAME=0,  @PHONE=0, @ADRESS=0, @ID=?"
                params=(delete_box.get())
                
                c.execute(storedProc, params)

                delete_box.delete(0, END)

                
                conn.commit()
                conn.close()
        # Создать функцию отправки для базы данных
        def submit():

                conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=ADELDOS;'
                              'Database=Courier_comp1;'
                              'Trusted_Connection=yes;')

                c = conn.cursor()

                storedProc = "exec company_proc @i=1, @NAME=?, @PHONE=?, @ADRESS=?, @ID=0"
                params=(NAME.get(),  PHONE.get(), ADRESS.get() )
                
                c.execute(storedProc, params)
                conn.commit()
                conn.close()

                # Очистить текстовые поля
                NAME.delete(0, END)
                PHONE.delete(0, END)
                ADRESS.delete(0, END)
                
        
                
        # Создать текстовые поля
        NAME = Entry(root3, width=30)
        NAME.grid(row=0, column=1, padx=20, pady=(10, 0))
        PHONE = Entry(root3, width=30)
        PHONE.grid(row=1, column=1)
        ADRESS = Entry(root3, width=30)
        ADRESS.grid(row=2, column=1)
        delete_box = Entry(root3, width=30)
        delete_box.grid(row=9, column=1, pady=5)

        # Создание меток текстовых полей
        NAME_label = Label(root3, text="Название компании")
        NAME_label.grid(row=0, column=0, pady=(10, 0))
        PHONE_label = Label(root3, text="телефон")
        PHONE_label.grid(row=1, column=0)
        ADRESS_label = Label(root3, text="Адрес")
        ADRESS_label.grid(row=2, column=0)
        delete_box_label = Label(root3, text="Выберите ID")
        delete_box_label.grid(row=9, column=0, pady=5)

        # Создать кнопку добавления
        submit_btn = Button(root3, text="Добавить запись", command=submit, bg="yellow")
        submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        # Создать кнопку показать
        query_btn = Button(root3, text="Показать все компании", command=show2, bg="yellow")
        query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=80)
        # Создать кнопку удаления
        delete_btn = Button(root3, text="Удалить запись", command=delete, bg="yellow")
        delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        # Создать кнопку обновления
        edit_btn = Button(root3, text="Изменить запись", command=edit, bg="yellow")
        edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=95)

        conn.commit()
        conn.close()

