from sqlite3 import connect
from datetime import date
from datetime import datetime as dt
from os import getcwd
from os import listdir
from os import mkdir
from sys import exit as exit_ex
from ttkthemes import ThemedTk
from tkinter.ttk import Frame
from tkinter.ttk import Notebook
from tkinter import TOP
from PIL import Image, ImageTk
from tkinter.ttk import Button
from tkinter.ttk import Label
from webbrowser import open

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

        self.style_ONE, self.style_TWO, self.list_record_ONE, self.list_record_TWO = self.create_list_values()

    def check_ico_download(self):
        pass

    def create_list_values(self):
        # Создаем список font для блоков
        self.cursor_sql.execute('SElECT * FROM list_block')
        list_values = self.cursor_sql.fetchall()
        list_one = [
            str(list_values[0][1]),
            str(list_values[0][2]),
            int(list_values[0][3]),
            str(f'{list_values[0][4]} {list_values[0][5]} {list_values[0][6]}')
        ]

        list_two = [
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


class Actions:
    pass


class Build_main_block:
    def __init__(self, main_block, help_png):
        pass


class Build_other_block:
    def __init__(self, main_block):
        pass


class Build_settings_block:
    def __init__(self, main_block):
        pass


class Build_report_block:
    def __init__(self, main_block):
        pass


class Build(Chek_value, Actions):
    def __init__(self):
        super().__init__()
        self.Main_window = ThemedTk(theme='black')
        self.Main_window.title('Справочник')
        self.Main_window.geometry('1200x500')
        x = (self.Main_window.winfo_screenwidth() - self.Main_window.winfo_reqwidth()) / 4
        y = (self.Main_window.winfo_screenheight() - self.Main_window.winfo_reqheight()) / 4
        self.Main_window.wm_geometry("+%d+%d" % (x - 50, y))

        # Создание картинок
        help_png_img = Image.open(f'{self.path_ico}/help.png')
        help_png = ImageTk.PhotoImage(help_png_img)

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

        self.btn_help = Button(self.main_block, text="Помощь",
                               cursor="X_cursor", command=lambda: self.Main_window.destroy()).pack()

        self.main_block = Build_main_block(self.main_block, help_png)

        self.Main_window.protocol("WM_DELETE_WINDOW", exit_ex)
        self.Main_window.mainloop()


while start:
    App = Build()
