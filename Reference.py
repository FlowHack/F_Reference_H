from sqlite3 import connect
from datetime import datetime as dt
from datetime import timedelta
from os import getcwd
from os import listdir
from os import mkdir
from os import path
from os.path import exists
from os.path import isfile
from os import name
from sys import exit as exit_ex
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPAuthenticationError
from smtplib import SMTP_SSL
from smtplib import SMTP
from ssl import create_default_context
from mimetypes import guess_type
from ttkthemes import ThemedTk
from tkinter.ttk import Frame
from tkinter.ttk import Notebook
from tkinter.ttk import Scrollbar
from tkinter.ttk import Entry
from tkinter.ttk import Combobox
from tkinter.ttk import Spinbox
from tkinter.ttk import Checkbutton
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename
from tkinter import WORD
from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import Text
from tkinter import Listbox
from tkinter import END
from tkinter import Toplevel
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter.ttk import Button
from tkinter.ttk import Label
from webbrowser import open as webopen

start: bool = True
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LANGUAGE = {
    'Russian': {
        'main_block': 'Главная',
        'other_block': 'Другое',
        'settings_block': 'Настройки',
        'report_block': 'Сообщить об ошибке или предложении',
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
        'set_onoff_other_block': 'Включить блок "Другое"',
        'set_language': 'Язык программы',
        'lab_rep_email': 'Email',
        'lab_rep_pas': 'Пароль',
        'lab_rep_addfile': 'Прикреп. файл',
        'lab_input_rep_addfile': 'Выберите файл, нажав на кнопку ==>',
        'lab_rep_text_vk': 'Вы можете написать мне во Вконтакте, нажмите ==>',
        'lbl_help_sait': 'Можете открыть помощь по программе на сайте, нажмите ==>',
        'lbl_add_main': 'Добавление записи в блок',
        'lbl_edit_main': 'Редактирование записи из блока',
        'lab_addedit_name': 'Название',
        'lab_addedit_font': 'Шрифт',
        'lab_addedit_size': 'Размер',
        'btn_addedit_apply': 'Применить к тексту',
        'btn_addedit_save': 'Сохранить',
        'send_email_great': 'Все отлично! Сообщение отправлено!',
        'send_email_wait': 'Если в течение 5-15 секунд это сообщение не отправится, то произошла ошибка!',
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
        'lab_set_name': 'Title',
        'lab_set_font': 'Font',
        'lab_set_size': 'Size',
        'input_set_bold': 'Boldface',
        'input_set_italic': 'Italics',
        'input_set_underline': 'Underline',
        'set_onoff_other_block': 'Enable the block "Other"',
        'set_language': 'Program language',
        'lab_rep_email': 'Email',
        'lab_rep_pas': 'Password',
        'lab_rep_addfile': 'Add attachment',
        'lab_input_rep_addfile': 'Select a file by clicking the button ==>',
        'lab_rep_text_vk': 'You can write on the social network Vkontakte, just click ==>',
        'lbl_help_sait': 'You can open the full and well-designed version of help, just click ==>',
        'lbl_add_main': 'Adding an entry to a block',
        'lbl_edit_main': 'Editing an entry from a block',
        'lab_addedit_name': 'Title',
        'lab_addedit_font': 'Font',
        'lab_addedit_size': 'Size',
        'btn_addedit_apply': 'To apply to the text',
        'btn_addedit_save': 'Save',
        'send_email_great': 'Everything is great! The message was sent!',
        'send_email_wait': 'If this message is not sent within 5-15 seconds, an error has occurred!',
    }
}
ERROR = {
    'Russian': {
        'delete': '''Произошла непредвиденная ошибка!

Возможно вы не выбрали удаляемую запись!

Если решить ошибку не удастся самостоятельно, то напишите в соответствующем блоке верхнего меню приложения. Хорошего дня!''',
        'addedit_name': '''Похоже, что длина введеного вами имени документа длиннее 40 сиволов!

Исправить эту ошибку! <Краткость - сестра таланта>''',
        'settings_title_ONE': '''Похоже, что длина введеного вами имени в первом документе длиннее 40 сиволов!

Исправьте эту ошибку! <Краткость - сестра таланта>''',
        'settings_title_TWO': '''Похоже, что длина введеного вами имени во втором документе длиннее 40 сиволов!

Исправьте эту ошибку! <Краткость - сестра таланта>''',
        'settings_title_is_empty_ONE': '''Похоже, что вы ввели пустую строку в навзании первого документа!
        
Исправьте эту ошибку! А то что-то слишком пусто получается :)''',
        'settings_title_is_empty_TWO': '''Похоже, что длина введеного вами имени во втором документе длиннее 40 сиволов!

Исправьте эту ошибку! <Краткость - сестра таланта>''',
        'report_gmail': """Неправильный логин или пароль!

Мы заметили, что вы отправляете сообщение с почты @gmail.com, возможно у вас запрещена отправка из неизвестных 
источников,тогда для решения проблемы перейдите по ссылке, которую мы сейчас добавили в текстовое поле,
и включите функцию отправки сообщений из неизвестных источников! Также вы можете использовать просто другую почту.

Внимание! После отправки сообщения обязательно выключите функцию на сайте!

Мы не несём ответственность за совершенные вами действия! """,
        'report_connect': """Произошла непредвиденная ошибка!
        
Пожалуйста, проверьте ваше подключение к сети, перезапустите программу. Если не получается исправить ошибку, 
то напишите об ошибке в соостветствующей вкладке приложения, мы поможем :)

Если не получается исправить ошибку, то напишите об ошибке в соостветствующей вкладке приложения, мы поможем :)""",
        'report_title_addr_is_empty': """Вы не заполнили поле EMAIL!
        
Заполните его, оно обязательно)""",
        'report_password_is_empty': """Вы не заполнили поле Пароль!
        
Заполните его, оно обязательно)""",
        'report_message_is_empty': """Вы не написали сообщение! Оно для вас шутка?
        
Заполните его, оно обязательно)""",
        'report_time': """В целях безопасности мы запретили отправлять сообщения чаше, чем 1 раз в час.
        
Можете написать через {time_ost:0.0f} мин.""",
        'report_message_too_short': """Вы написали слишком короткое сообщение, врятли вы смогли хорошо в нём изложить свою мысль!
        
Изложите её развёрнуто, не менее 30 символов! Нам ещё надо это понять и исправить!""",
    },
    'Englsh': {
        'delete': '''An unexpected error occurred!

You may not have selected the record to delete!

If you can't solve the error yourself, write in the corresponding block in the top menu of the app. Have a nice day!''',
        'addedit_name': '''It seems that the length you entered for the document name is longer than 40 character's!

Fix this error! < Brevity is the sister of talent>''',
        'settings_title_ONE': '''It seems that the length of the name you entered in the first document is longer than 40 sivolov!

Fix this error! < Brevity is the sister of talent>''',
        'settings_title_TWO': '''It seems that the length of the name you entered in the second document is longer than 40 sivolov!

Fix this error! < Brevity is the sister of talent>''',
        'settings_title_is_empty_ONE': '''It looks like you entered an empty string in the first document's title!
        
Fix this error! And then something is too empty turns out :)''',
        'settings_title_is_empty_TWO': '''It seems that the length of the name you entered in the second document is longer than 40 sivolov!

Fix this error! < Brevity is the sister of talent>''',
        'report_gmail': """Incorrect username or password!

We noticed that you are sending a message from your email @gmail.com, you may not be allowed to send from unknown sources 
so, to solve the problem, follow the link that we have now added to the text field,
and enable the function of sending messages from unknown sources!

Attention! After sending the message, be sure to turn off the function on the site!

We are not responsible for your actions!""",
        'report_connect': """An unexpected error occurred!

Please check your network connection and restart the program. If you can't fix the error, 
then write about the error in the corresponding tab of the app, we will help you :)

If you can't fix the error, then write about the error in the corresponding app tab, and we will help you :)""",
        'report_title_addr_is_empty': """You didn't fill in the EMAIL field!

Fill it out, it's mandatory)""",
        'report_password_is_empty': """You didn't fill in the Password field!

Fill it out, it's mandatory)""",
        'report_message_is_empty': """You didn't write the message! Is it a joke to you?

Fill it out, it's mandatory)""",
        'report_time': """For security reasons, we have forbidden sending messages more than 1 time per hour.

You can write via {time_ost:0.0 f} min.""",
        'report_message_too_short': """You wrote too short a message, I don't think you were able to Express your idea well in it!

State it in detail, at least 30 characters! We still need to understand and fix it!""",

    }
}
LANGUAGE_LIST = ['Russian', 'English']
FONT = ['Times New Roman', 'Calibri', 'Arial', 'Helvetica', 'Courier']
VALUE_MAIL = ['list.ru', 'bk.ru', 'inbox.ru', 'mail.ru', 'gmail.com']

class Chek_value:
    def __init__(self):
        self.path = getcwd()
        self.url_to_file = ''

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
            list_sqls = list(record[0] for record in self.cursor_sql.execute
            ('select name from sqlite_master where type = "table"').fetchall())
            self.chek_sql(list_sqls)

        else:
            self.connect_sql = connect(f'{self.path_settings}/settings.db')
            self.cursor_sql = self.connect_sql.cursor()
            self.completion_sql()

        self.value_ONE, self.value_TWO = self.create_list_values()
        self.list_record_ONE, self.list_record_TWO = self.create_value_records()

        self.start_other_block, self.launch, self.language, self.send_date = self.settings_app()[0]

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
            f'{list_values[0][4]} {list_values[0][5]} {list_values[0][6]}'
        ]

        list_two = [
            str(list_values[1][0]),
            str(list_values[1][1]),
            str(list_values[1][2]),
            int(list_values[1][3]),
            f'{list_values[1][4]} {list_values[1][5]} {list_values[1][6]}'
        ]

        return list_one, list_two

    def create_value_records(self):
        self.cursor_sql.execute('SElECT * FROM list_records')
        list_values = self.cursor_sql.fetchall()
        list_records_one = list(record for record in list_values if record[0] == 'ONE')
        list_records_two = list(record for record in list_values if record[0] == 'TWO')

        return list_records_one, list_records_two

    def sql_list_block(self):
        DEFAULT_VALUE_LIST = [
            ('ONE', 'Блок_1', 'Times New Roman', 12, 'bold', 'roman', ''),  # 40 8 16
            ('TWO', 'Блок_2', 'Times New Roman', 12, 'normal', 'italic', 'underline')
        ]
        self.cursor_sql.execute("""CREATE TABLE IF NOT EXISTS list_block(
                main_name TEXT,
                name TEXT,
                font TEXT,
                size INT,
                bolds TEXT,
                italics TEXT,
                underlines TEXT)""")
        self.connect_sql.commit()
        self.cursor_sql.executemany("INSERT INTO list_block VALUES (?,?,?,?,?,?,?)", DEFAULT_VALUE_LIST)
        self.connect_sql.commit()

    def sql_list_records(self):
        date = dt.now()
        DEFAULT_RECORDS_LIST = [
            ('ONE', 'Проверочная_запись_1', 'Проверочная_запись_1', 'Times New Roman', 12, date),
            ('TWO', 'Проверочная_запись_2', 'Проврочная_запись_2', 'Times New Roman', 12, date)
        ]
        self.cursor_sql.execute("""CREATE TABLE IF NOT EXISTS list_records(
                        name_list TEXT,
                        name TEXT,
                        text TEXT,
                        font TEXT,
                        size INT,
                        date TEXT)""")
        self.connect_sql.commit()
        self.cursor_sql.executemany("INSERT INTO list_records VALUES (?,?,?,?,?,?)", DEFAULT_RECORDS_LIST)
        self.connect_sql.commit()

    def sql_optimaze(self):
        self.cursor_sql.execute("""CREATE TABLE IF NOT EXISTS optimaze(
                        name TEXT,
                        turn_out INT)""")
        self.connect_sql.commit()

    def sql_settings(self):
        date = dt.now()

        self.cursor_sql.execute("""CREATE TABLE IF NOT EXISTS settings(
                                other_block BOOLEAN,
                                launch BOOLEAN,
                                language TEXT,
                                send_email TEXT)""")
        self.connect_sql.commit()
        self.cursor_sql.execute(
            f"INSERT INTO settings VALUES (True, True, 'Russian', '{(date - timedelta(hours=1)).strftime(DATE_FORMAT)}')")
        self.connect_sql.commit()

    def chek_sql(self, list_sql):
        if 'list_block' not in list_sql:
            self.sql_list_block()
        if 'list_records' not in list_sql:
            self.sql_list_records()
        if 'optimaze' not in list_sql:
            self.sql_optimaze()
        if 'settings' not in list_sql:
            self.sql_settings()

    def completion_sql(self):
        self.sql_list_block()
        self.sql_list_records()
        self.sql_optimaze()
        self.sql_settings()


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

    def curselection_identify(self, where):
        try:
            return str(where.get(where.curselection()).split()[1])
        except:
            showerror('Error', ERROR[self.language]['delete'])

    def completion_settings(self):
        def completion_bold_italic_underline(name, value, value_else):
            if name == bool(True):
                return value
            if name == bool(False):
                return value_else

        title_ONE, title_TWO = self.input_name_1.get(), self.input_name_2.get()
        font_ONE, font_TWO = self.input_font_1.get(), self.input_font_2.get()
        size_ONE, size_TWO = self.spinval_1.get(), self.spinval_2.get()
        bold_ONE = completion_bold_italic_underline(self.chk_bold_1.get(), 'bold', 'normal')
        bold_TWO = completion_bold_italic_underline(self.chk_bold_2.get(), 'bold', 'normal')
        italic_ONE = completion_bold_italic_underline(self.chk_italic_1.get(), 'italic', 'roman')
        italic_TWO = completion_bold_italic_underline(self.chk_italic_2.get(), 'italic', 'roman')
        underline_ONE = completion_bold_italic_underline(self.chk_underline_1.get(), 'underline', '')
        underline_TWO = completion_bold_italic_underline(self.chk_underline_2.get(), 'underline', '')
        other_block, language = self.chk_other_block.get(), self.input_language.get()

        try:
            if len(title_ONE) > 40:
                raise NameError('The first line is longer than 40')
            if len(title_TWO) > 40:
                raise NameError('The second line is longer than 40')
            if title_ONE == '':
                raise NameError('Empty string in the first')
            if title_TWO == '':
                raise NameError('Empty string in the second')

            self.cursor_sql.execute(f'''UPDATE list_block
                        SET name = "{title_ONE}",
                        font = "{font_ONE}",
                        size = {size_ONE},
                        bolds = "{bold_ONE}",
                        italics = "{italic_ONE}",
                        underlines = "{underline_ONE}"
                        WHERE main_name = "ONE"''')
            self.connect_sql.commit()
            self.cursor_sql.execute(f'''UPDATE list_block
                        SET name = "{title_TWO}",
                        font = "{font_TWO}",
                        size = {size_TWO},
                        bolds = "{bold_TWO}",
                        italics = "{italic_TWO}",
                        underlines = "{underline_TWO}"
                        WHERE main_name = "TWO"''')
            self.connect_sql.commit()
            self.cursor_sql.execute(f'''UPDATE settings
                                    SET other_block = {other_block},
                                    language = "{language}"''')
            self.connect_sql.commit()
            self.Main_window.destroy()
        except NameError as error:
            if str(error) == 'The first line is longer than 40':
                showerror('Error', ERROR[self.language]['settings_title_ONE'])
            if str(error) == 'The second line is longer than 40':
                showerror('Error', ERROR[self.language]['settings_title_TWO'])
            if str(error) == 'Empty string in the first':
                showerror('Error', ERROR[self.language]['settings_title_is_empty_ONE'])
            if str(error) == 'Empty string in the second':
                showerror('Error', ERROR[self.language]['settings_title_is_empty_TWO'])

    def delete_all(self):
        self.input_rep_expancion.delete(0, END)
        self.input_rep_pas.delete(0, END)
        self.input_rep_email.delete(0, END)
        self.send_date = dt.now().strftime(DATE_FORMAT)
        self.cursor_sql.execute(f'UPDATE settings SET send_email = "{self.send_date}"')
        self.connect_sql.commit()
        self.text_rep.delete(1.0, END)
        self.text_rep.insert(END, LANGUAGE[self.language]['send_email_great'])
        self.text_rep.config(fg='GREEN', font=('Times New Roman', 15, 'bold italic'))

    def sent_email(self):
        date = dt.now()
        time_difference = date - dt.strptime(self.send_date, DATE_FORMAT)
        time_difference_in_hour = time_difference / timedelta(hours=1)
        if round(time_difference_in_hour) >= 1:
            try:
                addr_from = self.input_rep_email.get()
                password = self.input_rep_pas.get()
                msg_text = self.text_rep.get(1.0, END)
                smtp_obj = self.input_rep_expancion.get()
                if addr_from == '':
                    raise NameError('Empty mail field')
                if password == '':
                    raise NameError('Empty password field')
                if msg_text == '':
                    raise NameError('Empty message field')
                if len(msg_text) < 30:
                    raise NameError('Message too short')
                url = self.url_to_file
                if smtp_obj in 'list.ru':
                    port = 'smtp.list.ru'
                elif smtp_obj == 'bk.ru':
                    port = 'smtp.bk.ru'
                elif smtp_obj == 'inbox.ru':
                    port = 'smtp.inbox.ru'
                elif smtp_obj == 'mail.ru':
                    port = 'smtp.mail.ru'
                elif smtp_obj == 'gmail.com':
                    port = 'smtp.gmail.com'

                def send_email(addr_to, addr_from, password, msg_text, files):

                    msg = MIMEMultipart()  # Создаем сообщение
                    msg['From'] = addr_from + '@' + smtp_obj  # Адресат
                    msg['To'] = addr_to  # Получатель
                    msg['Subject'] = 'F_Reference_H'  # Тема сообщения

                    body = msg_text  # Текст сообщения
                    msg.attach(MIMEText(body, 'plain'))

                    process_attachement(msg, files)

                    server = SMTP_SSL(port, 465)
                    self.text_rep.delete(1.0, END)
                    self.text_rep.insert(END, LANGUAGE[self.language]['send_email_wait'])
                    self.text_rep.config(fg='red', font=('Times New Roman', 15, 'bold italic'))
                    server.login(addr_from, password)
                    server.send_message(msg)
                    server.quit()
                    self.delete_all()

                def process_attachement(msg, files):
                    for f in files:
                        if isfile(f):
                            attach_file(msg, f)
                        elif exists(f):
                            dir = listdir(f)
                            for file in dir:
                                attach_file(msg, f + "/" + file)

                def attach_file(msg, filepath):
                    filename = path.basename(filepath)
                    ctype, encoding = guess_type(filepath)
                    if ctype is None or encoding is not None:
                        ctype = 'application/octet-stream'
                    maintype, subtype = ctype.split('/', 1)
                    if maintype == 'text':
                        with open(filepath) as fp:
                            file = MIMEText(fp.read(), _subtype=subtype)
                            fp.close()
                    elif maintype == 'image':
                        with open(filepath, 'rb') as fp:
                            file = MIMEImage(fp.read(), _subtype=subtype)
                            fp.close()
                    elif maintype == 'audio':
                        with open(filepath, 'rb') as fp:
                            file = MIMEAudio(fp.read(), _subtype=subtype)
                            fp.close()
                    else:
                        with open(filepath, 'rb') as fp:
                            file = MIMEBase(maintype, subtype)
                            file.set_payload(fp.read())
                            fp.close()
                            encoders.encode_base64(file)
                    file.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(file)

                addr_to = 'reference_auto@mail.ru'

                files = [fr'{url}']

                send_email(addr_to, addr_from, password, msg_text, files)
            except SMTPAuthenticationError:
                if port == 'smtp.gmail.com':
                    self.text_rep.delete(1.0, END)
                    self.text_rep.insert(END, 'https://myaccount.google.com/lesssecureapps')
                    self.text_rep.config(fg='RED', font=('Times New Roman', 15, 'bold italic'))
                    showerror('Error', ERROR[self.language]['report_gmail'])
            except NameError as error:
                if str(error) == 'Empty mail field':
                    showerror('Error', ERROR[self.language]['report_title_addr_is_empty'])
                if str(error) == 'Empty password field':
                    showerror('Error', ERROR[self.language]['report_password_is_empty'])
                if str(error) == 'Empty message field':
                    showerror('Error', ERROR[self.language]['report_message_is_empty'])
                if str(error) == 'Message too short':
                    showerror('Error', ERROR[self.language]['report_message_too_short'])
            except BaseException as error:
                if str(error) == '[Errno -3] Temporary failure in name resolution':
                    showerror('Error', ERROR[self.language]['report_connect'])
        else:
            showerror('Error', ERROR[self.language]['report_time'].format(time_ost=((1 - time_difference_in_hour)*60)))

    def searh_report_file(self):
        self.url_to_file = askopenfilename()
        self.lab_input_rep_addfile.configure(text=self.url_to_file, foreground='#BC8C5F')

    @staticmethod
    def open_webbrowser(url: str):
        webopen(url)


class Build(Chek_value, Actions):
    def __init__(self):
        super().__init__()
        self.Main_window = ThemedTk(theme='black')
        self.Main_window.title('F_Reference_H')
        self.Main_window.geometry('1200x500')
        x = (self.Main_window.winfo_screenwidth() - self.Main_window.winfo_reqwidth()) / 4
        y = (self.Main_window.winfo_screenheight() - self.Main_window.winfo_reqheight()) / 4
        self.Main_window.wm_geometry("+%d+%d" % (x - 50, y))
        self.Main_window.resizable(width=False, height=False)
        self.Main_window.iconphoto(True, PhotoImage(file='settings/ico/ico_main.png'))

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
        if self.start_other_block == 1:
            self.other_block = Frame(self.notebook)
        self.settings_block = Frame(self.notebook)
        self.report_block = Frame(self.notebook)
        self.help_block = Frame(self.notebook)
        self.notebook.add(self.main_block, text=LANGUAGE[self.language]['main_block'])
        if self.start_other_block == 1:
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
        self.add_1 = Button(self.frame_main_1, image=add_file, cursor='plus',
                            command=lambda: self.Add_edit('ADD', 'ONE')
                            ).place(
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
        self.add_2 = Button(self.frame_main_2, image=add_file, cursor='plus',
                            command=lambda: self.Add_edit('ADD', 'TWO')
                            ).place(
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

        self.list_block_1 = Listbox(self.main_block, cursor='dot')
        self.list_block_1.bind('<Double-Button-1>', lambda not_matter: self.Add_edit('EDIT', 'ONE',
                                                                                     self.curselection_identify(
                                                                                         self.list_block_1)))
        self.list_block_1['font'] = (self.value_ONE[2], self.value_ONE[3], self.value_ONE[4])
        self.list_block_1.place(y=40, relwidth=.5, relheight=0.91)
        self.scroll_list_block_1 = Scrollbar(self.list_block_1, orient='vertical')
        self.scroll_list_block_1.pack(side='right', fill='y')
        self.list_block_2 = Listbox(self.main_block, cursor='dot')
        self.list_block_2.bind('<Double-Button-1>', lambda not_matter: self.Add_edit('EDIT', 'TWO',
                                                                                     self.curselection_identify(
                                                                                         self.list_block_2)))
        self.list_block_2['font'] = (self.value_TWO[2], self.value_TWO[3], self.value_TWO[4])
        self.list_block_2.place(y=40, relx=.5005, relwidth=.5, relheight=0.91)
        self.scroll_list_block_2 = Scrollbar(self.list_block_2, orient='vertical')
        self.scroll_list_block_2.pack(side='right', fill='y')

# !!!!!!BUILD_OTHER_BLOCK!!!!!!
        if self.start_other_block == 1:
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
            self.optimaze_flowhack_1.bind('<Button-1>',
                                          lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))
            self.optimaze_flowhack_2 = Label(self.optimization_block, image=self.average_flowhack, cursor='heart')
            self.optimaze_flowhack_2.place(relx=.89, rely=.179)
            self.optimaze_flowhack_2.bind('<Button-1>',
                                          lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))

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
        self.spinval_1 = IntVar()
        self.spinval_1.set(self.value_ONE[3])
        self.input_size_1 = Spinbox(
            self.frame_optimization_1,
            from_=8,
            to=16,
            textvariable=self.spinval_1,
            font=('Times New Roman', 12, 'bold italic'),
            foreground='black',
            state='readonly'
        )
        self.input_size_1.place(relx=.2, y=150)
        self.chk_bold_1 = BooleanVar()
        if 'bold' in self.value_ONE[4]:
            self.chk_bold_1.set(bool(True))
        else:
            self.chk_bold_1.set(bool(False))
        self.input_set_bold_1 = Checkbutton(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['input_set_bold'],
            var=self.chk_bold_1
        ).place(relx=.05, y=250)
        self.chk_italic_1 = BooleanVar()
        if 'italic' in self.value_ONE[4]:
            self.chk_italic_1.set(bool(True))
        else:
            self.chk_italic_1.set(bool(False))
        self.input_set_italic_1 = Checkbutton(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['input_set_italic'],
            var=self.chk_italic_1
        ).place(relx=.3, y=250)
        self.chk_underline_1 = BooleanVar()
        if 'underline' in self.value_ONE[4]:
            self.chk_underline_1.set(bool(True))
        else:
            self.chk_underline_1.set(bool(False))
        self.input_set_underline_1 = Checkbutton(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['input_set_underline'],
            var=self.chk_underline_1
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
        self.spinval_2 = IntVar()
        self.spinval_2.set(self.value_TWO[3])
        self.input_size_2 = Spinbox(
            self.frame_optimization_2,
            from_=8,
            to=16,
            textvariable=self.spinval_2,
            font=('Times New Roman', 12, 'bold italic'),
            foreground='black',
            state='readonly'
        ).place(relx=.2, y=150)
        self.chk_bold_2 = BooleanVar()
        if 'bold' in self.value_TWO[4]:
            self.chk_bold_2.set(bool(True))
        else:
            self.chk_bold_2.set(bool(False))
        self.input_set_bold_2 = Checkbutton(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['input_set_bold'],
            var=self.chk_bold_2
        ).place(relx=.05, y=250)
        self.chk_italic_2 = BooleanVar()
        if 'italic' in self.value_TWO[4]:
            self.chk_italic_2.set(bool(True))
        else:
            self.chk_italic_2.set(bool(False))
        self.input_set_italic_2 = Checkbutton(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['input_set_italic'],
            var=self.chk_italic_2
        ).place(relx=.3, y=250)
        self.chk_underline_2 = BooleanVar()
        if 'underline' in self.value_TWO[4]:
            self.chk_underline_2.set(bool(True))
        else:
            self.chk_underline_2.set(bool(False))
        self.input_set_underline_2 = Checkbutton(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['input_set_underline'],
            var=self.chk_underline_2
        ).place(relx=.5, y=250)

        self.frame_optimization_3 = Frame(self.settings_block, borderwidth=2, relief='ridge')
        self.frame_optimization_3.place(relx=.025, rely=.6, relwidth=.95, relheight=.2)
        self.chk_other_block = BooleanVar()
        self.chk_other_block.set(bool(self.start_other_block))
        self.set_onoff_other_block = Checkbutton(
            self.frame_optimization_3,
            text=LANGUAGE[self.language]['set_onoff_other_block'],
            var=self.chk_other_block
        ).place(relx=.5, y=17, anchor='c')
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
        self.set_ok = Button(self.settings_block, image=ok, command=self.completion_settings).place(relx=.5, rely=.95,
                                                                                                    anchor='c')

# !!!!!! BUILD_REPORT_BLOCK !!!!!!
        Label(
            self.report_block,
            text=LANGUAGE[self.language]['lab_rep_email'],
            font=('Times New Roman', 12, 'bold italic'),
        ).place(y=10, relx=.01)
        self.input_rep_email = Entry(
            self.report_block,
            font=('Times New Roman', 11, 'bold italic'),
        )
        self.input_rep_email.place(relx=.08, y=10, relwidth=.15)
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
        )
        self.lab_input_rep_addfile.place(relx=.5, y=10, relwidth=.445)
        self.btn_rep_upload = Button(self.report_block, image=browse, command=self.searh_report_file).place(relx=.95,
                                                                                                            y=2)
        self.text_rep = Text(self.report_block, font=('Times New Roman', 12))
        self.text_rep.place(relx=.01, rely=.2, relheight=.785, relwidth=.982)
        self.lab_rep_text_vk = Label(
            self.report_block,
            font=('Times New Roman', 12, 'bold italic underline'),
            text=LANGUAGE[self.language]['lab_rep_text_vk']
        ).place(relx=.4, y=40)
        self.lab_rep_vk = Label(self.report_block, image=self.average_flowhack, cursor='heart')
        self.lab_rep_vk.place(relx=.75, y=36)
        self.lab_rep_vk.bind('<Button-1>', lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))
        self.btn_rep_send = Button(
            self.report_block,
            image=send,
            command=self.sent_email
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
        ).place(relx=.5, y=18, anchor='c')
        self.lbl_help_sait_png = Label(self.frame_help_1, image=self.sait, cursor='heart')
        self.lbl_help_sait_png.bind('<Button-1>', lambda no_matter: self.open_webbrowser('https://flowhack.github.io/'))
        self.lbl_help_sait_png.place(relx=.85, y=1)
        self.help_web = Text(self.help_block, font=('Times New Roman', 12))
        self.help_web.place(relx=.01, y=50, relheight=.87, relwidth=.98)

        self.completion_list(start_list=bool(False))
        self.Main_window.protocol("WM_DELETE_WINDOW", exit_ex)
        self.Main_window.mainloop()

    def Add_edit(self, doing, name_list, name_record=None):
        def apply():
            return self.text_addedit.configure(font=(self.input_addedit_font.get(), self.input_size_addedit.get()))

        def save():
            name = self.input_addedit_name.get()
            font = self.input_addedit_font.get()
            size = self.input_size_addedit.get()
            text = self.text_addedit.get(1.0, END)
            try:
                if len(name) > 40:
                    raise NameError

                if doing == 'EDIT':
                    self.cursor_sql.execute(f'''UPDATE list_records
                    SET name = "{name}",
                    text = "{text}",
                    font = "{font}",
                    size = {size}
                    WHERE (name = "{name_record}") and (name_list = "{name_list}")''')
                else:
                    self.cursor_sql.execute(
                        f'INSERT INTO list_records VALUES ("{name_list}",'
                        f' "{self.input_addedit_name.get()}",'
                        f' "{self.text_addedit.get(1.0, END)}",'
                        f' "{self.input_addedit_font.get()}",'
                        f' {self.input_size_addedit.get()},'
                        f' "{self.date_add}")'
                    )

                self.connect_sql.commit()
                self.Add_edit_window.destroy()
                self.completion_list()
            except NameError:
                showerror('Error', ERROR[self.language]['addedit_name'])

        if doing == 'ADD':
            self.date_add = dt.now().strftime('%d %B %Y %H:%M:%S')
            if name_list == 'ONE':
                text_main = f'{LANGUAGE[self.language]["lbl_add_main"]} <{self.value_ONE[1]}>'
            else:
                text_main = f'{LANGUAGE[self.language]["lbl_add_main"]} <{self.value_TWO[1]}>'
        else:
            text_main = f'{LANGUAGE[self.language]["lbl_edit_main"]} <{self.value_ONE[1]}>'
            self.cursor_sql.execute(f'SELECT * FROM list_records WHERE (name_list = "{name_list}") and '
                                    f'(name = "{name_record}")')
            addedit_all = self.cursor_sql.fetchone()

        self.Add_edit_window = Toplevel(background='#424242')
        self.Add_edit_window.title('Add_or_Edit')
        self.Add_edit_window.geometry('1200x950')
        x = (self.Add_edit_window.winfo_screenwidth() - self.Add_edit_window.winfo_reqwidth()) / 4
        y = (self.Add_edit_window.winfo_screenheight() - self.Add_edit_window.winfo_reqheight()) / 4
        self.Add_edit_window.wm_geometry("+%d+%d" % (x - 50, y - 180))
        self.Add_edit_window.bind('<Control-Key-s>', lambda no_matter: save())
        self.Add_edit_window.iconphoto(True, PhotoImage(file='settings/ico/ico_main.png'))

        frame = Frame(self.Add_edit_window, borderwidth=0.5, relief='solid')
        frame.place(relwidth=1, height=120)

        Label(self.Add_edit_window,
              text=text_main,
              font=('Times New Roman', 13, 'bold italic')
              ).place(relx=.5, y=20, anchor='c')
        label_flowhack_1 = Label(self.Add_edit_window, image=self.average_flowhack, cursor='heart')
        label_flowhack_1.bind('<Button-1>', lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))
        label_flowhack_1.place(relx=.1, anchor='c', y=20)
        label_flowhack_2 = Label(self.Add_edit_window, image=self.average_flowhack, cursor='heart')
        label_flowhack_2.bind('<Button-1>', lambda no_matter: self.open_webbrowser('http://vk.com/id311966436'))
        label_flowhack_2.place(relx=.9, anchor='c', y=20)
        Label(self.Add_edit_window,
              text=LANGUAGE[self.language]['lab_addedit_name'],
              font=('Times New Roman', 12, 'bold italic')
              ).place(x=10, y=50)
        self.input_addedit_name = Entry(self.Add_edit_window, font=('Times New Roman', 11, 'bold italic'))
        if doing == 'EDIT':
            self.input_addedit_name.insert(END, addedit_all[1])
        self.input_addedit_name.place(x=90, y=50, relwidth=.25, height=23)
        if doing == 'EDIT':
            Label(self.Add_edit_window,
                  text=addedit_all[5],
                  font=('Times New Roman', 12, 'bold italic')
                  ).place(x=10, y=90)
        else:
            Label(self.Add_edit_window,
                  text=self.date_add,
                  font=('Times New Roman', 12, 'bold italic')
                  ).place(x=10, y=90)
        Label(self.Add_edit_window,
              text=LANGUAGE[self.language]['lab_addedit_font'],
              font=('Times New Roman', 12, 'bold italic'),
              ).place(relx=.7, y=50)
        self.input_addedit_font = Combobox(
            self.Add_edit_window,
            font=('Times New Roman',
                  12,
                  'bold italic'),
            state='readonly')
        if doing == 'EDIT':
            self.input_addedit_font.set(addedit_all[3])
        else:
            self.input_addedit_font.set('Arial')
        self.input_addedit_font['values'] = FONT
        self.input_addedit_font.place(relx=.76, y=50, relwidth=.2, height=23)
        Label(self.Add_edit_window,
              font=('Times New Roman', 13, 'bold italic'),
              text=LANGUAGE[self.language]['lab_addedit_size']
              ).place(y=90, relx=.7)
        spinval_addedit = IntVar()
        if doing == 'EDIT':
            spinval_addedit.set(addedit_all[4])
        else:
            spinval_addedit.set(12)
        self.input_size_addedit = Spinbox(
            self.Add_edit_window,
            from_=8,
            to=16,
            textvariable=spinval_addedit,
            font=('Times New Roman', 12, 'bold italic'),
            foreground='black',
            state='readonly'
        )
        self.input_size_addedit.place(relx=.76, y=85, relwidth=.05)
        self.text_addedit = Text(
            self.Add_edit_window,
            wrap=WORD,
        )
        if doing == 'EDIT':
            self.text_addedit.insert(1.0, addedit_all[2])
            self.text_addedit['font'] = (addedit_all[3], addedit_all[4])
        self.text_addedit.place(y=120, relwidth=1, relheight=.8795)

        Button(self.Add_edit_window, text=LANGUAGE[self.language]['btn_addedit_apply'],
               command=lambda: apply()
               ).place(relx=.5, y=60, anchor='c')
        Button(self.Add_edit_window, text=LANGUAGE[self.language]['btn_addedit_save'],
               command=lambda: save()
               ).place(relx=.5, y=100, anchor='c')

        self.Add_edit_window.mainloop()


while start:
    App = Build()
