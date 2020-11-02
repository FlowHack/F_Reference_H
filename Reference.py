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
from tkinter.ttk import Entry
from tkinter.ttk import Combobox
from tkinter.ttk import Spinbox
from tkinter.ttk import Checkbutton
from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import Text
from tkinter import Listbox
from tkinter import END
from tkinter import Tk
from tkinter import Toplevel
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter.ttk import Button
from tkinter.ttk import Label
from webbrowser import open as webopen
from time import sleep

start: bool = True
DATE_FORMAT = '%d.%m.%Y'
LANGUAGE = {
    'Russian': {
        'main_block': 'Главная',
        'other_block': 'Другое',
        'settings_block': 'Настройки',
        'report_block': 'Сообщить об ошибке',
        'optimization_block': 'Оптимизация ID',
        'previously_created': 'Ранее созданные',
        'label_opt_main': 'Введите в поле ваши ID',
        'btn_optimaze': 'Оптимизировать',
        'lab_shortcat_id': 'Сочетания клавиш работают только на английской раскладке (<Ctrl+A> - Выделить всё, '
                           '<Ctrl+C> - Скопировать, <Ctrl+X> - Вырезать, <Ctrl+V> - Вставить)',
        'lab_set_name': 'Название',
        'lab_set_font': 'Шрифт',
        'lab_set_size': 'Размер',
        'input_set_bold': 'Жирный',
        'input_set_italic': 'Курсив',
        'input_set_underline': 'Подчёркивание',
        'set_onoff_other_block': 'Включить блок "Другое',
        'set_language': 'Язык программы',
        'lab_rep_email': 'Email',
        'lab_rep_pas': 'Пароль',
        'lab_rep_addfile': 'Прикрепить файл',
        'lab_input_rep_addfile': 'Выберите файл, нажав на кнопку ==>',
        'lab_rep_text_vk': 'Вы можете написать во Вконтакте, нажмите ==>',
        'lbl_help_sait': 'Вы можете открыть полную помощь по программе на сайте, нажмите ==>',
    },
    'English': {
        'main_block': 'Main',
        'other_block': 'Other',
        'settings_block': 'Settings',
        'report_block': 'Report a bug',
        'optimization_block': 'ID optimization',
        'previously_created': 'Previously created',
        'label_opt_main': 'Enter your ID in the field',
        'btn_optimaze': 'Optimize',
        'lab_shortcat_id': 'Keyboard shortcuts only work on the English keyboard layout (<Ctrl+A> - Select All, '
                           '<Ctrl+C> - Copy, <Ctrl+X> - Cut, <Ctrl+V> - Insert)',
        'lab_set_name': 'Name',
        'lab_set_font': 'Font',
        'lab_set_size': 'Size',
        'input_set_bold': 'Boldface',
        'input_set_italic': 'Italics',
        'input_set_underline': 'Underline',
        'set_onoff_other_block': 'Enable the block "Other"',
        'set_language': 'Program language',
    }
}
LANGUAGE_LIST = ['Russian', 'English']
FONT = ['Times New Roman', 'Calibri', 'Arial']
VALUE_MAIL = ['list.ru', 'bk.ru', 'inbox.ru', 'mail.ru', 'gmail.com']


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

        self.value_ONE, self.value_TWO = self.create_list_values()
        self.list_record_ONE, self.list_record_TWO = self.create_value_records()

        self.start_other_block, self.launch, self.language = self.settings_app()[0]

    def settings_app(self):
        self.cursor_sql.execute('SElECT * FROM settings')

        return self.cursor_sql.fetchall()

    def check_ico_download(self):
        self.cursor_sql.execute('SElECT * FROM list_block')

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

        return list_one, list_two

    def create_value_records(self):
        self.cursor_sql.execute('SElECT * FROM list_records')
        list_values = self.cursor_sql.fetchall()
        list_records_one = list(record for record in list_values if record[0] == 'ONE')
        list_records_two = list(record for record in list_values if record[0] == 'TWO')

        return list_records_one, list_records_two

    def chek_sql(self):
        DEFAULT_VALUE_LIST = [
            ('ONE', 'Блок_1', 'Times New Roman', 12, 'bold', 'roman', ''),  # 40 8 16
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
        self.cursor_sql.execute("""CREATE TABLE IF NOT EXISTS settings(
                        other_block BOOLEAN,
                        launch BOOLEAN,
                        language TEXT)""")
        self.connect_sql.commit()
        self.cursor_sql.execute("INSERT INTO settings VALUES (True, True, 'Russian')")
        self.connect_sql.commit()


class Actions:

    def completion_list(self, start_list=bool(True)):
        counter = 1
        self.list_block_1.delete(0, END)
        self.list_block_2.delete(0, END)

        if start_list:
            self.list_record_ONE, self.list_record_TWO = self.create_value_records()

        for record in self.list_record_ONE:
            self.list_block_1.insert(END, f' {counter}: {record[1]}')
        for record in self.list_record_TWO:
            self.list_block_2.insert(END, f' {counter}: {record[1]}')

    def copy_optimaze(self):
        pass
        # txt.clipboard_clear()  # Очистить буфер обмена
        # txt.clipboard_append(txt.get(1.0, END))

    def eyes(self, impossible=None):
        if self.eyes_value == bool(True):
            self.eyes_value = bool(False)
        else:
            self.eyes_value = bool(True)

        if self.eyes_value == bool(True):
            self.input_rep_pas.config(show='*')
            self.lab_rep_eyes.config(image=self.eye_close)
        else:
            self.input_rep_pas.config(show='')
            self.lab_rep_eyes.config(image=self.eye_open)

    def delete_record(self, name, record_name):
        self.cursor_sql.execute(f'DELETE FROM list_records WHERE name_list="{name}" and name="{record_name}"')
        self.connect_sql.commit()
        self.completion_list()

    @staticmethod
    def curselection_identify(where):
        return where.get(where.curselection()).split()[1]

    @staticmethod
    def open_webbrowser(url: str):
        webopen(url)


class Build(Chek_value, Actions):
    def __init__(self):
        # def starting():
        #     self.Main_window.deiconify()
        #     self.root.destroy()

        self.Main_window = ThemedTk(theme='black')
        # self.Main_window.withdraw()
        #
        # self.root = Toplevel()
        # self.root.geometry('+200+200')
        # self.root.overrideredirect(1)
        # Label(self.root, text='Программа запускается\n, терпение, только терпение').pack()
        #
        # self.Main_window.after(2000, starting)

        super().__init__()
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
        ok = Image.open(f'{self.path_ico}/ok.png')
        ok = ImageTk.PhotoImage(ok)
        eye_close = Image.open(f'{self.path_ico}/eyeclose.png')
        self.eye_close = ImageTk.PhotoImage(eye_close)
        eye_open = Image.open(f'{self.path_ico}/eyeopen.png')
        self.eye_open = ImageTk.PhotoImage(eye_open)
        send = Image.open(f'{self.path_ico}/send.png')
        send = ImageTk.PhotoImage(send)
        browse = Image.open(f'{self.path_ico}/browse.png')
        browse = ImageTk.PhotoImage(browse)
        sait = Image.open(f'{self.path_ico}/ico_main.png')
        self.sait = ImageTk.PhotoImage(sait)
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
        self.notebook.add(self.main_block, text=LANGUAGE[self.language]['main_block'])
        self.notebook.add(self.other_block, text=LANGUAGE[self.language]['other_block'])
        self.notebook.add(self.settings_block, text=LANGUAGE[self.language]['settings_block'])
        self.notebook.add(self.report_block, text=LANGUAGE[self.language]['report_block'])
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
        self.del_1 = Button(
            self.frame_main_1,
            image=trash,
            cursor='pirate',
            command=lambda: self.delete_record('ONE', self.curselection_identify(self.list_block_1))).place(
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
        self.update_1 = Button(self.frame_main_1, image=update, command=self.Main_window.destroy,
                               cursor='exchange'
                               ).place(
            rely=.11,
            relx=.825,
            width=32,
            height=26.2
        )
        self.name_list_2 = Label(self.frame_main_2, text=self.value_TWO[1])
        self.name_list_2.place(x=2, y=3)
        self.name_list_2['font'] = (self.value_TWO[2], self.value_TWO[3], self.value_TWO[4])
        self.del_2 = Button(
            self.frame_main_2,
            image=trash,
            cursor='pirate',
            command=lambda: self.delete_record('TWO', self.curselection_identify(self.list_block_2))
        ).place(
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
        self.update_2 = Button(self.frame_main_2, image=update, command=self.Main_window.destroy,
                               cursor='exchange'
                               ).place(
            rely=.11,
            relx=.825,
            width=32,
            height=26.2
        )

        # Создание ListBox
        self.list_block_1 = Listbox(self.main_block, cursor='dot')
        self.list_block_1.bind('<Double-Button-1>', lambda not_matter: self.curselection_identify(self.list_block_1))
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
        self.notebook_other.add(self.optimization_block, text=LANGUAGE[self.language]['optimization_block'])
        self.notebook_other.pack(expand=True, fill='both')

        # Заполнение optimaze
        self.previously_created = Button(
            self.optimization_block,
            text=LANGUAGE[self.language]['previously_created']
        ).place(y=5, x=1)
        self.label_opt_main = Label(self.optimization_block, text=LANGUAGE[self.language]['label_opt_main'])
        self.label_opt_main.place(y=10, relx=.5, anchor="c")
        self.label_opt_main['font'] = ('Times New Roman', 15, 'italic bold')
        self.btn_optimaze = Button(
            self.optimization_block,
            text=LANGUAGE[self.language]['btn_optimaze']
        ).place(y=5, relx=.888)
        Label(
            self.optimization_block,
            text=LANGUAGE[self.language]['lab_shortcat_id'],
            font=('Times New Roman', 10),
            foreground='red'
        ).place(relx=.5, rely=.22, anchor='c')
        self.id_text = Text(self.optimization_block)
        self.id_text.place(x=5, rely=.25, relwidth=.99, relheight=.738)
        self.optimaze_flowhack_1 = Label(self.optimization_block, image=self.average_flowhack, cursor='heart')
        self.optimaze_flowhack_1.place(x=5, rely=.175)
        self.optimaze_flowhack_1.bind('<Button-1>', lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))
        self.optimaze_flowhack_2 = Label(self.optimization_block, image=self.average_flowhack, cursor='heart')
        self.optimaze_flowhack_2.place(relx=.89, rely=.179)
        self.optimaze_flowhack_2.bind('<Button-1>', lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))

        # !!!!!! BUILD_SETTINGS_BLOCK !!!!!!

        self.frame_optimization_1 = Frame(self.settings_block, borderwidth=2, relief='ridge')
        self.frame_optimization_1.place(relwidth=.5, relheight=0.6)
        self.lab_set_1 = Label(self.frame_optimization_1, text=self.value_ONE[1])
        self.lab_set_1['font'] = (self.value_ONE[2], 12, self.value_ONE[4])
        self.lab_set_1.place(y=20, relx=.5, anchor='c')
        Label(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['lab_set_name'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=50)
        self.input_name_1 = Entry(self.frame_optimization_1, font=(self.value_ONE[2], 12))
        self.input_name_1.insert(END, self.value_ONE[1])
        self.input_name_1.place(y=50, relx=.2, relwidth=.6)
        Label(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['lab_set_font'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=100)
        self.input_font_1 = Combobox(
            self.frame_optimization_1,
            font=('Times New Roman',
                  12,
                  'bold italic'),
            state='readonly')
        self.input_font_1.set(self.value_ONE[2])
        self.input_font_1['values'] = FONT
        self.input_font_1.place(relx=.2, y=100, relwidth=.6)
        Label(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['lab_set_size'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=150)
        spinval_1 = IntVar()
        spinval_1.set(self.value_ONE[3])
        self.input_size_1 = Spinbox(
            self.frame_optimization_1,
            from_=8,
            to=16,
            textvariable=spinval_1,
            font=('Times New Roman', 12, 'bold italic'),
            foreground='black',
            state='readonly'
        )
        self.input_size_1.place(relx=.2, y=150)
        chk_bold_1 = BooleanVar()
        if 'bold' in self.value_ONE[4]:
            chk_bold_1.set(bool(True))
        else:
            chk_bold_1.set(bool(False))
        self.input_set_bold_1 = Checkbutton(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['input_set_bold'],
            var=chk_bold_1
        ).place(relx=.05, y=250)
        chk_italic_1 = BooleanVar()
        if 'italic' in self.value_ONE[4]:
            chk_italic_1.set(bool(True))
        else:
            chk_italic_1.set(bool(False))
        self.input_set_bold_1 = Checkbutton(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['input_set_italic'],
            var=chk_italic_1
        ).place(relx=.3, y=250)
        chk_underline_1 = BooleanVar()
        if 'italic' in self.value_ONE[4]:
            chk_underline_1.set(bool(True))
        else:
            chk_underline_1.set(bool(False))
        self.input_set_bold_1 = Checkbutton(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['input_set_underline'],
            var=chk_underline_1
        ).place(relx=.5, y=250)

        self.frame_optimization_2 = Frame(self.settings_block, borderwidth=2, relief='ridge')
        self.frame_optimization_2.place(relx=0.5, relwidth=.5, relheight=0.6)
        self.lab_set_2 = Label(self.frame_optimization_2, text=self.value_TWO[1])
        self.lab_set_2['font'] = (self.value_TWO[2], 12, self.value_TWO[4])
        self.lab_set_2.place(y=20, relx=.5, anchor='c')
        self.lab_set_2 = Label(self.frame_optimization_2, text=self.value_TWO[1])
        self.lab_set_2['font'] = (self.value_TWO[2], 12, self.value_TWO[4])
        self.lab_set_2.place(y=20, relx=.5, anchor='c')
        Label(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['lab_set_name'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=50)
        self.input_name_2 = Entry(self.frame_optimization_2, font=(self.value_TWO[2], 12))
        self.input_name_2.insert(END, self.value_TWO[1])
        self.input_name_2.place(y=50, relx=.2, relwidth=.6)
        self.lab_set_font_2 = Label(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['lab_set_font'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=100)
        self.input_font_2 = Combobox(
            self.frame_optimization_2,
            font=('Times New Roman',
                  12,
                  'bold italic'),
            state='readonly')
        self.input_font_2.set(self.value_TWO[2])
        self.input_font_2['values'] = FONT
        self.input_font_2.place(relx=.2, y=100, relwidth=.6)
        Label(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['lab_set_size'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=150)
        spinval_2 = IntVar()
        spinval_2.set(self.value_TWO[3])
        self.input_size_2 = Spinbox(
            self.frame_optimization_2,
            from_=8,
            to=16,
            textvariable=spinval_2,
            font=('Times New Roman', 12, 'bold italic'),
            foreground='black',
            state='readonly'
        ).place(relx=.2, y=150)
        chk_bold_2 = BooleanVar()
        if 'bold' in self.value_TWO[4]:
            chk_bold_2.set(bool(True))
        else:
            chk_bold_2.set(bool(False))
        self.input_set_bold_2 = Checkbutton(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['input_set_bold'],
            var=chk_bold_2
        ).place(relx=.05, y=250)
        chk_italic_2 = BooleanVar()
        if 'italic' in self.value_TWO[4]:
            chk_italic_2.set(bool(True))
        else:
            chk_italic_2.set(bool(False))
        self.input_set_bold_2 = Checkbutton(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['input_set_italic'],
            var=chk_italic_2
        ).place(relx=.3, y=250)
        chk_underline_2 = BooleanVar()
        if 'italic' in self.value_TWO[4]:
            chk_underline_2.set(bool(True))
        else:
            chk_underline_2.set(bool(False))
        self.input_set_bold_2 = Checkbutton(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['input_set_underline'],
            var=chk_underline_2
        ).place(relx=.5, y=250)

        self.frame_optimization_3 = Frame(self.settings_block, borderwidth=2, relief='ridge')
        self.frame_optimization_3.place(relx=.025, rely=.6, relwidth=.95, relheight=.2)
        chk_other_block = BooleanVar()
        chk_other_block.set(bool(self.start_other_block))
        self.set_onoff_other_block = Checkbutton(
            self.frame_optimization_3,
            text=LANGUAGE[self.language]['set_onoff_other_block'],
            var=chk_other_block
        ).place(relx=.5, y=10, anchor='c')
        Label(
            self.frame_optimization_3,
            font=('Times New Roman', 13, 'bold italic'),
            text=LANGUAGE[self.language]['set_language']
        ).place(relx=.44, y=50, anchor='c')
        self.input_language = Combobox(
            self.frame_optimization_3,
            font=('Times New Roman', 12, 'bold italic'),
            state='readonly'
        )
        self.input_language.set(self.language)
        self.input_language['values'] = LANGUAGE_LIST
        self.input_language.place(relx=.59, y=50, anchor='c')
        self.set_ok = Button(self.settings_block, image=ok).place(relx=.5, rely=.95, anchor='c')

        # !!!!!! BUILD_SETTINGS_BLOCK !!!!!!
        Label(
            self.report_block,
            text=LANGUAGE[self.language]['lab_rep_email'],
            font=('Times New Roman', 12, 'bold italic'),
        ).place(y=10, relx=.01)
        self.input_rep_email = Entry(
            self.report_block,
            font=('Times New Roman', 11, 'bold italic'),
        ).place(relx=.08, y=10, relwidth=.15)
        Label(
            self.report_block,
            font=('Times New Roman', 13, 'bold italic'),
            text='@'
        ).place(relx=.225, y=7)
        self.input_rep_expancion = Combobox(
            self.report_block,
            font=('Times New Roman', 11, 'bold italic'),
            state='readonly'
        )
        self.input_rep_expancion.set('mail.ru')
        self.input_rep_expancion['values'] = VALUE_MAIL
        self.input_rep_expancion.place(y=10, relx=.24)
        Label(
            self.report_block,
            font=('Times New Roman', 12, 'bold italic'),
            text=LANGUAGE[self.language]['lab_rep_pas']
        ).place(relx=.01, y=40)
        self.input_rep_pas = Entry(
            self.report_block,
            font=('Times New Roman', 11, 'bold italic'),
            show='*'
        )
        self.input_rep_pas.place(relx=.08, y=40, relwidth=.25)
        self.lab_rep_eyes = Label(
            self.report_block,
            image=self.eye_close
        )
        self.lab_rep_eyes.place(y=34, relx=.34)
        self.eyes_value: bool = True
        self.lab_rep_eyes.bind('<Button-1>', self.eyes)
        self.lab_rep_addfile = Label(
            self.report_block,
            font=('Times New Roman', 12, 'bold italic'),
            text=LANGUAGE[self.language]['lab_rep_addfile']
        ).place(relx=.4, y=10)
        self.lab_input_rep_addfile = Label(
            self.report_block,
            font=('Times New Roman', 11, 'bold'),
            foreground='black',
            text=LANGUAGE[self.language]['lab_input_rep_addfile'],
            borderwidth=0.5,
            relief='solid'
        ).place(relx=.515, y=10, relwidth=.43)
        self.btn_rep_upload = Button(self.report_block, image=browse).place(relx=.95, y=2)
        self.text_rep = Text(self.report_block, font=('Times New Roman', 12))
        self.text_rep.place(relx=.01, rely=.2, relheight=.785, relwidth=.982)
        self.lab_rep_text_vk = Label(
            self.report_block,
            font=('Times New Roman', 12, 'bold italic underline'),
            text=LANGUAGE[self.language]['lab_rep_text_vk']
        ).place(relx=.4, y=40)
        self.lab_rep_vk = Label(self.report_block, image=self.average_flowhack, cursor='heart')
        self.lab_rep_vk.place(relx=.73, y=36)
        self.lab_rep_vk.bind('<Button-1>', lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))
        self.btn_rep_send = Button(
            self.report_block,
            image=send
        ).place(relx=.951, y=51)
        self.lbl_set_flowhack_1 = Label(self.settings_block, image=self.max_flowhack, cursor='heart')
        self.lbl_set_flowhack_1.bind('<Button-1>', lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))
        self.lbl_set_flowhack_1.place(relx=.05, rely=.92)
        self.lbl_set_flowhack_2 = Label(self.settings_block, image=self.max_flowhack, cursor='heart')
        self.lbl_set_flowhack_2.bind('<Button-1>', lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))
        self.lbl_set_flowhack_2.place(relx=.81, rely=.92)

        # !!!!!! BUILD_HELP_BLOCK !!!!!!
        self.frame_help_1 = Frame(self.help_block, borderwidth=0.5, relief='solid')
        self.frame_help_1.place(relx=.5, y=20, relwidth=.6, height=40, anchor='c')
        Label(
            self.frame_help_1,
            text=LANGUAGE[self.language]['lbl_help_sait'],
            font=('Times New Roman', 12, 'bold italic')
        ).place(relx=.05, y=7)
        self.lbl_help_sait_png = Label(self.frame_help_1, image=self.sait, cursor='heart')
        self.lbl_help_sait_png.bind('<Button-1>', lambda no_matter: self.open_webbrowser('https://flowhack.github.io/'))
        self.lbl_help_sait_png.place(relx=.85, y=1)
        self.help_web = Text(self.help_block, font=('Times New Roman', 12))
        self.help_web.place(relx=.01, y=50, relheight=.87, relwidth=.98)

        self.completion_list(start_list=bool(False))
        self.Main_window.protocol("WM_DELETE_WINDOW", exit_ex)
        self.Main_window.mainloop()


while start:
    App = Build()
