from sqlite3 import connect
from datetime import date
from datetime import datetime as dt
from os import getcwd
from os import listdir
from os import mkdir
from os import path
from os import name
from sys import exit as exit_ex
from ttkthemes import ThemedTk
from tkinter.ttk import Frame
from tkinter.ttk import Notebook
from tkinter.ttk import Scrollbar
from tkinter import Text
from tkinter import Listbox
from tkinter import END
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter.ttk import Button
from tkinter.ttk import Label
from webbrowser import open as webopen

start: bool = True
DATE_FORMAT = '%d.%m.%Y'


class Chek_value:
    def __init__(self):
        self.path = getcwd()

        # Create folder settings
        if 'settings' in listdir(self.path):
            self.path_settings = f'{self.path}/settings'
        else:
            mkdir(f'{self.path}/settings')
            self.path_settings = f'{self.path}/settings'

        # Create folder ico
        if 'ico' in listdir(self.path_settings):
            self.path_ico = f'{self.path_settings}/ico'
        else:
            mkdir(f'{self.path_settings}/ico')
            self.path_ico = f'{self.path_settings}/ico'

        # Create SQL
        if 'settings.db' in listdir(self.path_settings):
            self.connect_sql = connect(f'{self.path_settings}/settings.db')
            self.cursor_sql = self.connect_sql.cursor()
        else:
            self.connect_sql = connect(f'{self.path_settings}/settings.db')
            self.cursor_sql = self.connect_sql.cursor()
            self.chek_sql()

        self.value_ONE, self.value_TWO, self.list_record_ONE, self.list_record_TWO = self.create_list_values()

    def check_ico_download(self):
        pass

    def create_list_values(self):
        # Создаем список font для блоков
        self.cursor_sql.execute('SElECT * FROM list_block')
        list_values = self.cursor_sql.fetchall()
        list_one = [
            str(list_values[0][0]),
            str(list_values[0][1]),
            str(list_values[0][2]),
            int(list_values[0][3]),
            str(f'{list_values[0][4]} {list_values[0][5]} {list_values[0][6]}')
        ]

        list_two = [
            str(list_values[1][0]),
            str(list_values[1][1]),
            str(list_values[1][2]),
            int(list_values[1][3]),
            str(f'{list_values[1][4]} {list_values[1][5]} {list_values[1][6]}')
        ]
        # Создаем список font для редактора
        self.cursor_sql.execute('SElECT * FROM list_records')
        list_values = self.cursor_sql.fetchall()
        list_records_one = list(record for record in list_values if record[0] == 'ONE')
        list_records_two = list(record for record in list_values if record[0] == 'TWO')
        return list_one, list_two, list_records_one, list_records_two

    def chek_sql(self):
        DEFAULT_VALUE_LIST = [
            ('ONE', 'Блок_1', 'Times New Roman', 12, 'bold', 'roman', ''),
            ('TWO', 'Блок_2', 'Times New Roman', 12, 'normal', 'italic', 'underline')
        ]
        DEFAULT_RECORDS_LIST = [
            ('ONE', 'Проверочная_запись_1', 'Проверочная_запись_1', 'Times New Roman', 12, date.today()),
            ('TWO', 'Проверочная_запись_2', 'Проврочная_запись_2', 'Times New Roman', 12, date.today())
        ]
        self.cursor_sql.execute("""CREATE TABLE IF NOT EXISTS list_block(
        main_name TEXT,
        name TEXT,
        font TEXT,
        size INT,
        bold TEXT,
        italic TEXT,
        underline TEXT)""")
        self.connect_sql.commit()
        self.cursor_sql.execute("""CREATE TABLE IF NOT EXISTS list_records(
                name_list TEXT,
                name TEXT,
                text TEXT,
                font TEXT,
                size INT,
                date DATE)""")
        self.connect_sql.commit()
        self.cursor_sql.executemany("INSERT INTO list_block VALUES (?,?,?,?,?,?,?)", DEFAULT_VALUE_LIST)
        self.connect_sql.commit()
        self.cursor_sql.executemany("INSERT INTO list_records VALUES (?,?,?,?,?,?)", DEFAULT_RECORDS_LIST)
        self.connect_sql.commit()
        self.cursor_sql.execute("""CREATE TABLE IF NOT EXISTS optimaze(
                name TEXT,
                turn_out INT)""")
        self.connect_sql.commit()


class Actions:
    def completion_list(self):
        counter = 1
        self.list_block_1.delete(0, END)
        self.list_block_2.delete(0, END)

        for record in self.list_record_ONE:
            self.list_block_1.insert(END, f'{counter}: {record[1]}')
        for record in self.list_record_TWO:
            self.list_block_2.insert(END, f'{counter}: {record[1]}')

    def copy_optimaze(self):
        pass
        # txt.clipboard_clear()  # Очистить буфер обмена
        # txt.clipboard_append(txt.get(1.0, END))

    def open_flowhack_vk(self, uncessary=None):
        uncessary = None
        webopen('http://vk.com/id311966436')


class Build(Chek_value, Actions):
    # cursor = "heart"
    # cursor="sizing"
    def __init__(self):
        super().__init__()
        self.Main_window = ThemedTk(theme='black')
        self.Main_window.title('F_Reference_H')
        self.Main_window.geometry('1200x500')
        x = (self.Main_window.winfo_screenwidth() - self.Main_window.winfo_reqwidth()) / 4
        y = (self.Main_window.winfo_screenheight() - self.Main_window.winfo_reqheight()) / 4
        self.Main_window.wm_geometry("+%d+%d" % (x - 50, y))
        self.Main_window.resizable(width=False, height=False)
        self.Main_window.iconphoto(True, PhotoImage(file=path.join(self.path_ico, "ico_main.png")))

        # Создание картинок
        help_png_img = Image.open(f'{self.path_ico}/help.png')
        help_png = ImageTk.PhotoImage(help_png_img)
        trash = Image.open(f'{self.path_ico}/trash.png')
        trash = ImageTk.PhotoImage(trash)
        add_file = Image.open(f'{self.path_ico}/add_file.png')
        add_file = ImageTk.PhotoImage(add_file)
        update = Image.open(f'{self.path_ico}/update.png')
        update = ImageTk.PhotoImage(update)
        max_flowhack = Image.open(f'{self.path_ico}/max_flowhack.png')
        self.max_flowhack = ImageTk.PhotoImage(max_flowhack)
        average_flowhack = Image.open(f'{self.path_ico}/average_flowhack.png')
        self.average_flowhack = ImageTk.PhotoImage(average_flowhack)
        mini_flowhack = Image.open(f'{self.path_ico}/mini_flowhack.png')
        self.mini_flowhack = ImageTk.PhotoImage(mini_flowhack)

        self.notebook = Notebook(self.Main_window)
        self.main_block = Frame(self.notebook)
        self.other_block = Frame(self.notebook)
        self.settings_block = Frame(self.notebook)
        self.report_block = Frame(self.notebook)
        self.help_block = Frame(self.notebook)
        self.notebook.add(self.main_block, text='Главная')
        self.notebook.add(self.other_block, text='Другое')
        self.notebook.add(self.settings_block, text='Настройки')
        self.notebook.add(self.report_block, text='Написать об ошибке')
        self.notebook.add(self.help_block, image=help_png)
        self.notebook.pack(expand=True, fill='both')

        # !!!!!!BUILD_MAIN_BLOCK!!!!!!

        self.frame_main_1 = Frame(self.main_block, borderwidth=0.5, relief='solid')
        self.frame_main_1.place(relwidth=.5, height=35)
        self.frame_main_2 = Frame(self.main_block, borderwidth=0.5, relief='solid')
        self.frame_main_2.place(relx=.5, relwidth=.5, height=35)

        # Наполнение frame
        self.name_list_1 = Label(self.frame_main_1, text=self.value_ONE[1])
        self.name_list_1.place(x=2, y=3)
        self.name_list_1['font'] = (self.value_ONE[2], self.value_ONE[3], self.value_ONE[4])
        self.del_1 = Button(self.frame_main_1, image=trash, cursor='pirate').place(
            rely=.11,
            relx=.94,
            width=32,
            height=26.2
        )
        self.add_1 = Button(self.frame_main_1, image=add_file, cursor='plus').place(
            rely=.11,
            relx=.882,
            width=32,
            height=26.2
        )
        self.update_1 = Button(self.frame_main_1, image=update, command=self.completion_list, cursor='exchange').place(
            rely=.11,
            relx=.825,
            width=32,
            height=26.2
        )
        self.name_list_2 = Label(self.frame_main_2, text=self.value_TWO[1])
        self.name_list_2.place(x=2, y=3)
        self.name_list_2['font'] = (self.value_TWO[2], self.value_TWO[3], self.value_TWO[4])
        self.del_2 = Button(self.frame_main_2, image=trash, cursor='pirate').place(
            rely=.11,
            relx=.94,
            width=32,
            height=26.2
        )
        self.add_2 = Button(self.frame_main_2, image=add_file, cursor='plus').place(
            rely=.11,
            relx=.882,
            width=32,
            height=26.2
        )
        self.update_2 = Button(self.frame_main_2, image=update, command=self.completion_list, cursor='exchange').place(
            rely=.11,
            relx=.825,
            width=32,
            height=26.2
        )

        # Создание ListBox
        self.list_block_1 = Listbox(self.main_block, cursor='dot')
        self.list_block_1['font'] = (self.value_ONE[2], self.value_ONE[3], self.value_ONE[4])
        self.list_block_1.place(y=40, relwidth=.5, relheight=0.91)
        self.scroll_list_block_1 = Scrollbar(self.list_block_1, orient='vertical')
        self.scroll_list_block_1.pack(side='right', fill='y')
        self.list_block_2 = Listbox(self.main_block, cursor='dot')
        self.list_block_2['font'] = (self.value_TWO[2], self.value_TWO[3], self.value_TWO[4])
        self.list_block_2.place(y=40, relx=.5005, relwidth=.5, relheight=0.91)
        self.scroll_list_block_2 = Scrollbar(self.list_block_2, orient='vertical')
        self.scroll_list_block_2.pack(side='right', fill='y')

        # !!!!!!BUILD_OTHER_BLOCK!!!!!!
        self.notebook_other = Notebook(self.other_block)
        self.optimization_block = Frame(self.notebook_other)
        self.notebook_other.add(self.optimization_block, text='Оптимизация ID')
        self.notebook_other.pack(expand=True, fill='both')

        # Заполнение optimaze
        self.previously_created = Button(self.optimization_block, text='Ранее созданные').place(y=5, x=1)
        self.label_opt_main = Label(self.optimization_block, text='Введите в поле ваши ID')
        self.label_opt_main.place(y=5, relx=.41)
        self.label_opt_main['font'] = ('Times New Roman', 15, 'italic bold')
        self.btn_optimaze = Button(self.optimization_block, text='Оптимизировать').place(y=5, relx=.888)
        self.lab_shortcat_id = Label(
            self.optimization_block,
            text='Сочетания клавиш работают только на английской раскладке (<Ctrl+A> - Выделить всё, <Ctrl+C> - '
                 'Скопировать, <Ctrl+X> - Вырезать, <Ctrl+V> - Вставить)'
        )
        self.lab_shortcat_id.place(x=145, rely=.2)
        self.lab_shortcat_id['font'] = ('Times New Roman', 10)
        self.lab_shortcat_id['foreground'] = 'red'
        self.id_text = Text(self.optimization_block)
        self.id_text.place(x=5, rely=.25, relwidth=.99, relheight=.738)
        self.optimaze_flowhack_1 = Label(self.optimization_block, image=self.average_flowhack, cursor='heart')
        self.optimaze_flowhack_1.place(x=5, rely=.175)
        self.optimaze_flowhack_1.bind('<Button-1>', self.open_flowhack_vk)
        self.optimaze_flowhack_2 = Label(self.optimization_block, image=self.average_flowhack, cursor='heart')
        self.optimaze_flowhack_2.place(relx=.89, rely=.179)
        self.optimaze_flowhack_2.bind('<Button-1>', self.open_flowhack_vk)

        self.completion_list()
        self.Main_window.protocol("WM_DELETE_WINDOW", exit_ex)
        self.Main_window.mainloop()


while start:
    App = Build()
