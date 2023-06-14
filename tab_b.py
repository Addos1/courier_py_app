import tkinter as tk
import pyodbc
from tkinter import *
import tkinter.ttk as ttk

class Example(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
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
                c.execute("exec output @i=5")
                records = c.fetchall()
                for i, (id_EXP1, FK_CUR, FK_CLI,  NUM_EXP,  DATE_EXP, SIGN) in enumerate(records, start=1):
                    listBox.insert("", "end", values=(id_EXP1, FK_CUR, FK_CLI,  NUM_EXP,  DATE_EXP, SIGN))
                conn.close()

        def show2 ():      
                global editor
                editor = Tk()
                editor.title('Экспресс накладная')
                cols = ('Id', 'Получатель', 'Отправитель', 'Номер Экспресс накладной', 'Дата', 'Подпись')
                listBox =ttk.Treeview(editor, columns=cols, show='headings')
                for col in cols:
                    listBox.heading(col, text=col)    
                    listBox.grid(row=1, column=0, columnspan=2)
                closeButton = tk.Button(editor, text="Закрыть", width=15, command=editor.destroy, bg="yellow").grid(row=6, column=1)
                show(listBox)

        def showExp2(listBox1):
                conn1 = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')
                # создать курсор
                c1 =conn1.cursor()
                storedProc1 = "exec exp2_proc2 @i=1,@ID=?"
                params1=(delete_box.get())
                c1.execute(storedProc1, params1)
                
                records1 = c1.fetchall()
                for i, ( FK_EXP1, FK_PROD, PRICE, SUM_PROD, PRICE_SUM_PROD) in enumerate(records1, start=1):
                    listBox1.insert("", "end", values=( FK_EXP1, FK_PROD, PRICE, SUM_PROD,PRICE_SUM_PROD))
                conn1.close()

        def showExp2_2 ():      
                global editor1
                editor1 = Tk()
                editor1.title('Экспресс накладная2')

                cols1 = ('Id', 'Товар', 'Цена', 'Количество', 'Сумма')
                listBox1 =ttk.Treeview(editor1, columns=cols1, show='headings')
                for col in cols1:
                    listBox1.heading(col, text=col)    
                    listBox1.grid(row=1, column=0, columnspan=2)
                closeButton1 = tk.Button(editor1, text="Закрыть", width=15, command=editor1.destroy, bg="yellow").grid(row=5, column=1)
                showExp2(listBox1)

        def update():
                        conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')
                        c = conn.cursor()
                        record_id = delete_box.get()                       
                        # Запрос базы данных
                        storedProc = "exec exp2_proc @i=2, @fk_prod=?, @sum_prod=?, @price=?, @ID=?"
                        params=(fk_prod_editor.get(),  sum_prod_editor.get(), price_editor.get(), record_id)                        
                        c.execute(storedProc, params)
                        #зафиксировать изменения
                        conn.commit()
                        # остановить связь с базой данных
                        conn.close()
                        editor.destroy()

        def edit():
                       
                        global editor
                        editor = Tk()
                        editor.title('Добавитть товар')
                        editor.geometry("350x170")
                        conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')
                        c = conn.cursor()
                        record_id = delete_box.get()                 
                        #Создание глобальных переменных для имен текстовых полей
                        global fk_prod_editor
                        global sum_prod_editor
                        global price_editor
                        # Создать текстовые поля
                        fk_prod_editor = Entry(editor, width=30)
                        fk_prod_editor.grid(row=0, column=1)
                        sum_prod_editor = Entry(editor, width=30)
                        sum_prod_editor.grid(row=1, column=1)
                        price_editor = Entry(editor, width=30)
                        price_editor.grid(row=2, column=1)                                      
                        # Создание меток текстовых полей
                        fk_prod_label = Label(editor, text="ID продукта")
                        fk_prod_label.grid(row=0, column=0)
                        sum_prod_label = Label(editor, text="Количество")
                        sum_prod_label.grid(row=1, column=0)
                        price_label = Label(editor, text="Цена")
                        price_label.grid(row=2, column=0)                        
                        # Создать кнопку «Сохранить» для сохранения отредактированной записи
                        edit_btn = Button(editor, text="Сохранить запись", command=update,bg="yellow" )
                        edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

                # Создать функцию отправки для базы данных
        def submit():

                        conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=ADELDOS;'
                                      'Database=Courier_comp1;'
                                      'Trusted_Connection=yes;')

                        c = conn.cursor()
                        storedProc = "exec exp1_proc @i=1, @FK_CUR=?, @FK_CLI=?,  @NUM_EXP=?,  @DATE_EXP=?, @SIGN=1, @ID=0"
                        params=(FK_CUR.get(),  FK_CLI.get(), NUM_EXP.get(),  DATE_EXP.get() )                        
                        c.execute(storedProc, params)
                        conn.commit()
                        conn.close()
                        # Очистить текстовые поля
                        FK_CUR.delete(0, END)
                        FK_CLI.delete(0, END)
                        NUM_EXP.delete(0, END)
                        DATE_EXP.delete(0, END)
                                                           
                # Создать текстовые поля
        FK_CUR = Entry(self, width=30)
        FK_CUR.grid(row=0, column=1, padx=20, pady=(10, 0))
        FK_CLI = Entry(self, width=30)
        FK_CLI.grid(row=1, column=1)
        NUM_EXP = Entry(self, width=30)
        NUM_EXP.grid(row=2, column=1)
        DATE_EXP = Entry(self, width=30)
        DATE_EXP.grid(row=3, column=1)
       
        delete_box = Entry(self, width=30)
        delete_box.grid(row=9, column=1, pady=5)
                # Создание меток текстовых полей
        FK_CUR_label = Label(self, text="ID курьера")
        FK_CUR_label.grid(row=0, column=0, pady=(10, 0))
        FK_CLI_label = Label(self, text="ID клиента")
        FK_CLI_label.grid(row=1, column=0)
        NUM_EXP_label = Label(self, text="Номер Экспресс накладной")
        NUM_EXP_label.grid(row=2, column=0)
        DATE_EXP_label = Label(self, text="Дата")
        DATE_EXP_label.grid(row=3, column=0)
     
        delete_box_label = Label(self, text="Выберите ID Экспресс накладной")
        delete_box_label.grid(row=9, column=0, pady=5)
                # Создать кнопку добавления
        submit_btn = Button(self, text="Добавить запись", command=submit, bg="yellow")
        submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
                # Создать кнопку показать
        query_btn = Button(self, text="Показать все экспресс накладные", command=show2, bg="yellow")
        query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=55)
                # Создать кнопку удаления
        delete_btn = Button(self, text="Показать проданные товары", command=showExp2_2, bg="yellow")
        delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=70)
                # Создать кнопку обновления
        edit_btn = Button(self, text="Добавить товар", command=edit, bg="yellow")
        edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=102)
        conn.commit()
        conn.close()
        self.pack()

  
