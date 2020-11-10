from datetime import datetime as dt
from datetime import timedelta
from random import choice
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mimetypes import guess_type
from os import getcwd, listdir, mkdir, path
from os.path import exists, isfile
from smtplib import SMTP_SSL, SMTPAuthenticationError
from sqlite3 import connect
from sys import exit as exit_ex
from tkinter import (END, WORD, BooleanVar, IntVar, Listbox, PhotoImage,
                     StringVar, Text, Toplevel, DISABLED, NORMAL)
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.ttk import (Button, Checkbutton, Combobox, Entry, Frame, Label,
                         Notebook, Radiobutton, Scrollbar, Spinbox)
from webbrowser import open as webopen

from PIL import Image, ImageTk
from ttkthemes import ThemedTk

start: bool = True
VERSION = '1'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LANGUAGE = {
    'Russian': {
        'main_block': 'Главная',
        'other_block': 'Другое',
        'settings_block': 'Настройки',
        'report_block': 'Обратная связь',
        'optimization_block': 'Оптимизация ID',
        'previously_created': 'Ранее созданные',
        'label_opt_main': 'Введите в поле ваши ID',
        'btn_optimaze': 'Оптимизировать',
        'lab_shortcat_id': 'Сочетания клавиш могут не работать на русской раскладке (<Ctrl+A> - Выделить всё, <Ctrl+C> - Скопировать, <Ctrl+X> - Вырезать, <Ctrl+V> - Вставить)',
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
        'lbl_help_sait': 'Можете открыть помощь по программе на сайте, '
                         'нажмите ==>',
        'lbl_add_main': 'Добавление записи в блок',
        'lbl_edit_main': 'Редактирование записи из блока',
        'lab_addedit_name': 'Название',
        'lab_addedit_font': 'Шрифт',
        'lab_addedit_size': 'Размер',
        'btn_addedit_apply': 'Применить к тексту',
        'btn_addedit_save': 'Сохранить',
        'send_email_great': 'Все отлично! Сообщение отправлено!',
        'send_email_wait': 'Если в течение 5-15 секунд это сообщение не '
                           'отправится, то произошла ошибка!',
        'label_opt_main_id': 'Всего получилось: ',
        'btn_optimaze_copy': 'Скопировать поле',
        'format_optimize_1': 'https://vk.com/id+значение',
        'format_optimize_2': '@id+значение',
        'format_optimize_3': 'id+значение',
        'format_optimize_4': 'значение',
        'format_optimize': 'Форматы вывода',
        'optimizee_name': 'Название',
        'optimizee_date': 'Дата создания',
        'del_old_optimize': 'Удалить старые записи',
        'del_all_optimize': 'Удалить все записи',
        'HELP_TEXT': 'Всю необходимую помощь Вы можете найти на сайте https://flowhack.github.io/\nПо использованию программы, дополнительных функциях, горячих клавишах и т.д.',
        'HELP_SAIT': 'Скопировать сылку',
        'pas_generator_block': 'Генератор паролей',
        'pas_generator_main_title': 'Сгенерируем пароль!',
        'pas_generator_result': 'Ваш пароль:',
        'pas_generator_count_symbols': 'Количество символов',
        'pas_generator_symbols': 'Использовать дополнительные сиволы',
        'pas_generator_number': 'Использовать цифры',
        'pas_generator_upper': 'Использовать заглавные буквы',
        'pas_generator_sha1': 'SHA1',
        'pas_generator_md5': 'MD5',
        'pas_generator_sha224': 'SHA224',
        'pas_generator_sha256': 'SHA256',
        'pas_generator_sha384': 'SHA384',
        'pas_generator_sha512': 'SHA512',
        'pas_generator_blake2b': 'BLAKE2b',
        'pas_generator_blake2s': 'BLAKE2s',
        'pas_generator_sha3_384': 'SHA3_384',
        'pas_generator_sha3_512': 'SHA3_512',
        'pas_generator_shake_128': 'SHAKE_128',
        'pas_generator_shake_256': 'SHAKE_256',
        'pas_generator_copy': 'Скопировать пароль'
    },
    'English': {
    }
}
ERROR = {
    'Russian': {
        'delete': 'Произошла непредвиденная ошибка!\n\nВы не выбрали запись!',
        'addedit_name': 'Похоже, что длина введеного вами имени документа длиннее 40 сиволов!\n\nИсправьте эту ошибку! <Краткость - сестра таланта>',
        'settings_title_ONE': 'Похоже, что длина введеного вами имени в первом документе длиннее 40 сиволов!\n\nИсправьте эту ошибку! <Краткость - сестра таланта>',
        'settings_title_TWO': 'Похоже, что длина введеного вами имени во втором документе длиннее 40 сиволов!\n\nИсправьте эту ошибку! <Краткость - сестра таланта>',
        'settings_title_is_empty_ONE': 'Похоже, что вы ввели пустую строку в навзании первого документа!\n\nИсправьте эту ошибку! А то что-то слишком пусто получается :)',
        'settings_title_is_empty_TWO': 'Похоже, что вы ввели пустую строку в названии второго документа!\n\nИсправьте эту ошибку! <Краткость - сестра таланта>',
        'report_gmail': 'Неправильный логин или пароль!\n\nМы заметили, что вы отправляете сообщение с почты @gmail.com, возможно у вас запрещена отправка из неизвестных источников,тогда для решения проблемы перейдите по ссылке, которую мы сейчас добавили в текстовое поле, и включите функцию отправки сообщений из неизвестных источников! Также вы можете использовать просто другую почту.\n\nВнимание! После отправки сообщения обязательно выключите функцию на сайте! Мы не несём ответственность за совершенные вами действия!',
        'report_connect': 'Произошла непредвиденная ошибка!\n\nПожалуйста, проверьте ваше подключение к сети, перезапустите программу. Если не получается исправить ошибку, то напишите об ошибке в соостветствующей вкладке приложения, мы поможем :)\n\nЕсли не получается исправить ошибку, то напишите об ошибке в соостветствующей вкладке приложения, мы поможем :)',
        'report_title_addr_is_empty': 'Вы не заполнили поле EMAIL!\n\nЗаполните его, оно обязательно)',
        'report_password_is_empty': 'Вы не заполнили поле Пароль!\n\nЗаполните его, оно обязательно)',
        'report_message_is_empty': 'Вы не написали сообщение! Оно для вас шутка?\n\nЗаполните его, оно обязательно)',
        'report_time': 'В целях безопасности мы запретили отправлять сообщения чаше, чем 1 раз в час.\n\nМожете написать через {time_ost:0.0f} мин.',
        'report_message_too_short': 'Вы написали слишком короткое сообщение, врятли вы смогли хорошо в нём изложить свою мысль!\n\nИзложите её развёрнуто, не менее 30 символов! Нам ещё надо это понять и исправить!',
        'unacceptable_symbols': 'Вы использовали недопустимые символы! (:;!*#¤&)'
    },
    'Englsh': {

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
            list_sqls = list(
                record[0]
                for record in
                self.cursor_sql.execute('''SELECT name 
                                        FROM sqlite_master 
                                        WHERE type = "table"'''
                                        ).fetchall()
            )
            self.chek_sql(list_sqls)

        else:
            self.connect_sql = connect(f'{self.path_settings}/settings.db')
            self.cursor_sql = self.connect_sql.cursor()
            self.completion_sql()

        self.value_ONE, self.value_TWO = self.create_list_values()
        self.list_record_ONE, self.list_record_TWO = \
            self.create_value_records()

        self.start_other_block, self.launch, self.language, self.send_date = \
            self.settings_app()[0]

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
        list_records_one = list(
            record for record in list_values if record[0] == 'ONE'
        )
        list_records_two = list(
            record for record in list_values if record[0] == 'TWO'
        )

        return list_records_one, list_records_two

    def sql_list_block(self):
        DEFAULT_VALUE_LIST = [
            ('ONE', 'Блок_1', 'Times New Roman', 12, 'bold', 'roman', ''),
            # 40 8 16
            ('TWO', 'Блок_2', 'Times New Roman', 12, 'normal', 'italic',
             'underline')
        ]
        self.cursor_sql.execute(
            '''CREATE TABLE IF NOT EXISTS list_block(
            main_name TEXT,
            name TEXT,
            font TEXT,
            size INT,
            bolds TEXT,
            italics TEXT,
            underlines TEXT)'''
        )
        self.connect_sql.commit()
        self.cursor_sql.executemany(
            'INSERT INTO list_block VALUES (?,?,?,?,?,?,?)',
            DEFAULT_VALUE_LIST
        )
        self.connect_sql.commit()

    def sql_list_records(self):
        date = dt.now().strftime(DATE_FORMAT)
        DEFAULT_RECORDS_LIST = [
            (
                'ONE',
                'Проверочная_запись_1',
                'Проверочная_запись_1',
                'Times New Roman',
                12,
                date
            ),
            (
                'TWO',
                'Проверочная_запись_2',
                'Проврочная_запись_2',
                'Times New Roman',
                12,
                date
            )
        ]
        self.cursor_sql.execute(
            '''CREATE TABLE IF NOT EXISTS list_records(
            name_list TEXT,
            name TEXT,
            text TEXT,
            font TEXT,
            size INT,
            date TEXT)'''
        )
        self.connect_sql.commit()
        self.cursor_sql.executemany(
            'INSERT INTO list_records VALUES (?,?,?,?,?,?)',
            DEFAULT_RECORDS_LIST
        )
        self.connect_sql.commit()

    def sql_optimaze(self):
        self.cursor_sql.execute(
            '''CREATE TABLE IF NOT EXISTS optimaze(
            name INTEGER PRIMARY KEY,
            turn_out INT,
            date TEXT,
            text TEXT)'''
        )
        self.connect_sql.commit()

    def sql_settings(self):
        date = dt.now()

        self.cursor_sql.execute(
            '''CREATE TABLE IF NOT EXISTS settings(
            other_block BOOLEAN,
            launch BOOLEAN,
            language TEXT,
            send_email TEXT)'''
        )
        self.connect_sql.commit()
        self.cursor_sql.execute(
            f'''INSERT INTO settings VALUES (True, True, "Russian", 
            "{(date - timedelta(hours=1)).strftime(DATE_FORMAT)}")'''
        )
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

        if start_list: self.list_record_ONE, self.list_record_TWO = \
            self.create_value_records()

        for record in self.list_record_ONE:
            self.list_block_1.insert(END, f' {counter}: {record[1]}')
        for record in self.list_record_TWO:
            self.list_block_2.insert(END, f' {counter}: {record[1]}')

    def copy_optimaze(self):
        self.id_text.clipboard_clear()
        self.id_text.clipboard_append(self.id_text.get(1.0, END))

    def copy_help(self):
        self.btn_help_copy.clipboard_clear()
        self.btn_help_copy.clipboard_append('https://flowhack.github.io/')

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
        self.cursor_sql.execute(
            f'''DELETE FROM list_records 
            WHERE name_list="{name}" and name="{record_name}"'''
        )
        self.connect_sql.commit()
        self.completion_list()

    def curselection_identify(self, where):
        try:
            return str(where.get(where.curselection()).split(': ')[1])
        except BaseException as error:
            if str(error) == 'bad listbox index "": must be active, anchor, ' \
                             'end, @x,y, or a number':
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
        bold_ONE = completion_bold_italic_underline(
            self.chk_bold_1.get(),
            'bold',
            'normal'
        )
        bold_TWO = completion_bold_italic_underline(
            self.chk_bold_2.get(),
            'bold',
            'normal'
        )
        italic_ONE = completion_bold_italic_underline(
            self.chk_italic_1.get(),
            'italic',
            'roman'
        )
        italic_TWO = completion_bold_italic_underline(
            self.chk_italic_2.get(),
            'italic',
            'roman'
        )
        underline_ONE = completion_bold_italic_underline(
            self.chk_underline_1.get(),
            'underline',
            ''
        )
        underline_TWO = completion_bold_italic_underline(
            self.chk_underline_2.get(),
            'underline', ''
        )
        other_block, language = \
            self.chk_other_block.get(), self.input_language.get()

        try:
            if len(title_ONE) > 40:
                raise NameError('The first line is longer than 40')
            if len(title_TWO) > 40:
                raise NameError('The second line is longer than 40')
            if title_ONE == '':
                raise NameError('Empty string in the first')
            if title_TWO == '':
                raise NameError('Empty string in the second')

            self.cursor_sql.execute(
                f'''UPDATE list_block
                SET name = "{title_ONE}",
                font = "{font_ONE}",
                size = {size_ONE},
                bolds = "{bold_ONE}",
                italics = "{italic_ONE}",
                underlines = "{underline_ONE}"
                WHERE main_name = "ONE"'''
            )
            self.connect_sql.commit()
            self.cursor_sql.execute(
                f'''UPDATE list_block
                SET name = "{title_TWO}",
                font = "{font_TWO}",
                size = {size_TWO},
                bolds = "{bold_TWO}",
                italics = "{italic_TWO}",
                underlines = "{underline_TWO}"
                WHERE main_name = "TWO-"'''
            )
            self.connect_sql.commit()
            self.cursor_sql.execute(
                f'''UPDATE settings
                SET other_block = {other_block},
                language = "{language}"'''
            )
            self.connect_sql.commit()
            self.Main_window.destroy()
        except NameError as error:
            if str(error) == 'The first line is longer than 40':
                showerror('Error', ERROR[self.language]['settings_title_ONE'])
            if str(error) == 'The second line is longer than 40':
                showerror('Error', ERROR[self.language]['settings_title_TWO'])
            if str(error) == 'Empty string in the first':
                showerror('Error',
                          ERROR[self.language]['settings_title_is_empty_ONE'])
            if str(error) == 'Empty string in the second':
                showerror('Error',
                          ERROR[self.language]['settings_title_is_empty_TWO'])

    def delete_all(self):
        self.input_rep_expancion.delete(0, END)
        self.input_rep_pas.delete(0, END)
        self.input_rep_email.delete(0, END)
        self.send_date = dt.now().strftime(DATE_FORMAT)
        self.cursor_sql.execute(
            f'UPDATE settings SET send_email = "{self.send_date}"')
        self.connect_sql.commit()
        self.text_rep.delete(1.0, END)
        self.text_rep.insert(END, LANGUAGE[self.language]['send_email_great'])
        self.text_rep.config(
            fg='GREEN',
            font=('Times New Roman', 15, 'bold italic')
        )
        self.text_rep.after(
            5000,
            self.text_rep.config(
                fg='white',
                font=('Times New Roman', 12, 'bold italic'))
        )

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
                    self.text_rep.insert(
                        END,
                        LANGUAGE[self.language]['send_email_wait']
                    )
                    self.text_rep.config(
                        fg='red',
                        font=('Times New Roman', 15, 'bold italic')
                    )
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
                    file.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=filename
                    )
                    msg.attach(file)

                addr_to = 'reference_auto@mail.ru'

                files = [fr'{url}']

                send_email(addr_to, addr_from, password, msg_text, files)
            except SMTPAuthenticationError:
                if port == 'smtp.gmail.com':
                    self.text_rep.delete(1.0, END)
                    self.text_rep.insert(
                        END,
                        'https://myaccount.google.com/lesssecureapps'
                    )
                    self.text_rep.config(
                        fg='RED',
                        font=('Times New Roman', 15, 'bold italic')
                    )
                    showerror('Error', ERROR[self.language]['report_gmail'])
            except NameError as error:
                if str(error) == 'Empty mail field':
                    showerror(
                        'Error',
                        ERROR[self.language]['report_title_addr_is_empty']
                    )
                if str(error) == 'Empty password field':
                    showerror(
                        'Error',
                        ERROR[self.language]['report_password_is_empty']
                    )
                if str(error) == 'Empty message field':
                    showerror(
                        'Error',
                        ERROR[self.language]['report_message_is_empty']
                    )
                if str(error) == 'Message too short':
                    showerror(
                        'Error',
                        ERROR[self.language]['report_message_too_short']
                    )
            except BaseException as error:
                if str(error) == '[Errno -3] Temporary failure in name ' \
                                 'resolution':
                    showerror('Error', ERROR[self.language]['report_connect'])
        else:
            showerror(
                'Error',
                ERROR[self.language]['report_time'].format(
                    time_ost=((1 - time_difference_in_hour) * 60))
            )

    def searh_report_file(self):
        self.url_to_file = askopenfilename()
        self.lab_input_rep_addfile.configure(
            text=self.url_to_file,
            foreground='#BC8C5F'
        )

    def move(self, name_list):
        if name_list == 'ONE':
            name = self.curselection_identify(self.list_block_1)
            name_list_move = 'TWO'
        else:
            name = self.curselection_identify(self.list_block_2)
            name_list_move = 'ONE'

        if name != None:
            self.cursor_sql.execute(
                f'''UPDATE list_records
                SET name_list = "{name_list_move}"
                WHERE (name_list = "{name_list}") and 
                (name = "{name}")'''
            )
            self.connect_sql.commit()

            self.completion_list()

    def optimize_id(self):
        def optimize_result(record_list, formats):
            finish = []
            for result_record in record_list:
                if result_record[:2] == 'id':
                    result_value = int(result_record[2:])
                    if result_value > 100:
                        finish.append(formats + result_record[2:])
                elif result_record[:3] == '@id':
                    result_value = int(result_record[3:])
                    if result_value > 100:
                        finish.append(formats + result_record[3:])
                elif result_record[:17] == 'https://vk.com/id':
                    result_value = int(result_record[17:])
                    if result_value > 100:
                        finish.append(formats + result_record[17:])
                else:
                    result_value = int(result_record)
                    if result_value > 100:
                        finish.append(formats + result_record)

            _finish = '\n'.join(set(finish))
            return _finish, len(finish)

        record = self.id_text.get(1.0, END).split()
        format = self.format_optimize_var.get()
        result_finish = optimize_result(record, format)
        if result_finish != '':
            date_now = dt.now().strftime(DATE_FORMAT)
            self.id_text.delete(1.0, END)
            self.id_text.insert(1.0, result_finish[0])
            self.cursor_sql.execute(
                f'''INSERT INTO optimaze (turn_out, date, text) VALUES 
                ("{str(result_finish[1])}", "{date_now}", 
                "{result_finish[0]}")'''
            )
            self.label_opt_main.configure(
                text=LANGUAGE[self.language]['label_opt_main_id'] + str(
                    result_finish[1]),
                foreground='#FF757F'
            )
            self.label_opt_main.after(
                3000,
                lambda: self.label_opt_main.configure(
                    text=LANGUAGE[self.language]['label_opt_main'],
                    foreground='white')
            )

    def optimization_open(self, name_value):
        if name_value is not None:
            self.cursor_sql.execute(
                f'SELECT text,turn_out FROM optimaze WHERE name="{name_value}"'
            )
            optimization_record = self.cursor_sql.fetchone()
            self.id_text.delete(1.0, END)
            self.id_text.insert(1.0, optimization_record[0])
            self.label_opt_main.configure(
                text=LANGUAGE[self.language]['label_opt_main_id'] + str(
                    optimization_record[1]),
                foreground='#FF757F'
            )
            self.label_opt_main.after(
                5000,
                lambda: self.label_opt_main.configure(
                    text=LANGUAGE[self.language]['label_opt_main'],
                    foreground='white'
                )
            )
            self.optimizee_window.destroy()

    def password_generate(self):
        main_list_symbols: list = ['a', 'b', 'c', 'd', 'i', 'f', 'g', 'h',
                                   'i', 'g', 'k', 'l', 'm', 'n', 'o', 'p',
                                   'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                                   'y', 'z']
        additional_symbols: list = ['!', '.', ',', '@', '#', '$', '%', '?',
                                    '*']
        number_symbols: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        upper_symbols: list = ['A', 'B', 'C', 'D', 'I', 'F', 'G', 'H', 'I',
                               'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if self.chk_pas_symbol:
            main_list_symbols += additional_symbols
        if self.chk_pas_number:
            main_list_symbols += number_symbols
        if self.chk_pas_upper:
            main_list_symbols += upper_symbols


    @staticmethod
    def open_webbrowser(url: str):
        webopen(url)


class Build(Chek_value, Actions):
    def __init__(self):
        super().__init__()
        self.Main_window = ThemedTk(theme='black')
        self.Main_window.title('F_Reference_H')
        self.Main_window.geometry('1200x500')
        x = (self.Main_window.winfo_screenwidth() -
             self.Main_window.winfo_reqwidth()) / 4
        y = (self.Main_window.winfo_screenheight() -
             self.Main_window.winfo_reqheight()) / 4
        self.Main_window.wm_geometry("+%d+%d" % (x - 50, y))
        self.Main_window.resizable(width=False, height=False)
        self.Main_window.iconphoto(True, PhotoImage(
            file='settings/ico/ico_main.png'))

        help_png_img = Image.open(f'{self.path_ico}/help.png')
        help_png = ImageTk.PhotoImage(help_png_img)
        trash = Image.open(f'{self.path_ico}/trash.png')
        self.trash = ImageTk.PhotoImage(trash)
        add_file = Image.open(f'{self.path_ico}/add_file.png')
        add_file = ImageTk.PhotoImage(add_file)
        update = Image.open(f'{self.path_ico}/update.png')
        update = ImageTk.PhotoImage(update)
        ok = Image.open(f'{self.path_ico}/ok.png')
        ok = ImageTk.PhotoImage(ok)
        move = Image.open(f'{self.path_ico}/move.png')
        move = ImageTk.PhotoImage(move)
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
        self.notebook.add(
            self.main_block,
            text=LANGUAGE[self.language]['main_block']
        )
        if self.start_other_block == 1:
            self.notebook.add(
                self.other_block,
                text=LANGUAGE[self.language]['other_block']
            )
        self.notebook.add(
            self.settings_block,
            text=LANGUAGE[self.language]['settings_block']
        )
        self.notebook.add(
            self.report_block,
            text=LANGUAGE[self.language]['report_block']
        )
        self.notebook.add(self.help_block, image=help_png)
        self.notebook.pack(expand=True, fill='both')

        # !!!!!!BUILD_MAIN_BLOCK!!!!!!

        self.frame_main_1 = Frame(
            self.main_block,
            borderwidth=0.5,
            relief='solid'
        )
        self.frame_main_1.place(relwidth=.5, height=35)
        self.frame_main_2 = Frame(
            self.main_block,
            borderwidth=0.5,
            relief='solid'
        )
        self.frame_main_2.place(relx=.5, relwidth=.5, height=35)

        self.name_list_1 = Label(self.frame_main_1, text=self.value_ONE[1])
        self.name_list_1.place(x=2, y=3)
        self.name_list_1['font'] = (
            self.value_ONE[2],
            self.value_ONE[3],
            self.value_ONE[4]
        )
        self.del_1 = Button(
            self.frame_main_1,
            image=self.trash,
            cursor='pirate',
            command=lambda: self.delete_record(
                'ONE',
                self.curselection_identify(self.list_block_1)
            )
        ).place(
            rely=.11,
            relx=.94,
            width=32,
            height=26.2
        )
        self.add_1 = Button(
            self.frame_main_1,
            image=add_file,
            cursor='plus',
            command=lambda: self.Add_edit('ADD', 'ONE')
        ).place(rely=.11, relx=.882, width=32, height=26.2)
        self.update_1 = Button(
            self.frame_main_1,
            image=update,
            command=self.Main_window.destroy,
            cursor='exchange'
        ).place(rely=.11, relx=.825, width=32, height=26.2)
        self.move_1 = Button(
            self.frame_main_1,
            image=move,
            cursor='right_side',
            command=lambda: self.move('ONE')
        ).place(rely=.11, relx=.768, width=32, height=26.2)
        self.name_list_2 = Label(
            self.frame_main_2,
            text=self.value_TWO[1]
        )
        self.name_list_2.place(x=2, y=3)
        self.name_list_2['font'] = (
            self.value_TWO[2],
            self.value_TWO[3],
            self.value_TWO[4]
        )
        self.del_2 = Button(
            self.frame_main_2,
            image=self.trash,
            cursor='pirate',
            command=lambda: self.delete_record(
                'TWO',
                self.curselection_identify(self.list_block_2)
            )
        ).place(rely=.11, relx=.94, width=32, height=26.2)
        self.add_2 = Button(
            self.frame_main_2,
            image=add_file,
            cursor='plus',
            command=lambda: self.Add_edit('ADD', 'TWO')
        ).place(rely=.11, relx=.882, width=32, height=26.2)
        self.update_2 = Button(
            self.frame_main_2, image=update,
            command=self.Main_window.destroy,
            cursor='exchange'
        ).place(rely=.11, relx=.825, width=32, height=26.2)
        self.move_2 = Button(
            self.frame_main_2,
            image=move,
            cursor='left_side',
            command=lambda: self.move('TWO')
        ).place(rely=.11, relx=.768, width=32, height=26.2)

        self.list_block_1 = Listbox(
            self.main_block,
            cursor='dot',
            selectbackground='#f3be81',
            background='#232629',
            foreground='#B6B6B6',
            highlightcolor='black'
        )
        self.list_block_1.bind(
            '<Double-Button-1>',
            lambda not_matter: self.Add_edit(
                'EDIT',
                'ONE',
                self.curselection_identify(self.list_block_1)
            )
        )
        self.list_block_1.bind(
            '<Button-2>',
            lambda no_matter: self.move('ONE')
        )
        self.list_block_1['font'] = (
            self.value_ONE[2],
            self.value_ONE[3],
            self.value_ONE[4]
        )
        self.list_block_1.place(y=40, relwidth=.5, relheight=0.91)
        self.scroll_list_block_1 = Scrollbar(
            self.list_block_1,
            orient='vertical'
        )
        self.scroll_list_block_1.pack(side='right', fill='y')
        self.list_block_2 = Listbox(
            self.main_block,
            cursor='dot',
            selectbackground='#f3be81',
            background='#232629',
            foreground='#B6B6B6',
            highlightcolor='black'
        )
        self.list_block_2.bind(
            '<Double-Button-1>',
            lambda not_matter: self.Add_edit(
                'EDIT',
                'TWO',
                self.curselection_identify(self.list_block_2)
            )
        )
        self.list_block_2.bind(
            '<Button-2>',
            lambda no_matter: self.move('TWO')
        )
        self.list_block_2['font'] = (
            self.value_TWO[2],
            self.value_TWO[3],
            self.value_TWO[4]
        )
        self.list_block_2.place(y=40, relx=.5005, relwidth=.5, relheight=0.91)
        self.scroll_list_block_2 = Scrollbar(
            self.list_block_2,
            orient='vertical'
        )
        self.scroll_list_block_2.pack(side='right', fill='y')

        # !!!!!!BUILD_OTHER_BLOCK!!!!!!
        if self.start_other_block == 1:
            self.notebook_other = Notebook(self.other_block)
            self.optimization_block = Frame(self.notebook_other)
            self.pas_generator_block = Frame(self.notebook_other)
            self.notebook_other.add(
                self.optimization_block,
                text=LANGUAGE[self.language]['optimization_block']
            )
            self.notebook_other.add(
                self.pas_generator_block,
                text=LANGUAGE[self.language]['pas_generator_block']
            )
            self.notebook_other.pack(expand=True, fill='both')

            # Заполнение optimaze
            self.previously_created = Button(
                self.optimization_block,
                text=LANGUAGE[self.language]['previously_created'],
                command=self.Optimize_records,
                cursor='hand1'
            ).place(y=5, x=1)
            self.label_opt_main = Label(
                self.optimization_block,
                text=LANGUAGE[self.language][
                    'label_opt_main']
            )
            self.label_opt_main.place(y=10, relx=.5, anchor="c")
            self.label_opt_main['font'] = (
                'Times New Roman',
                15,
                'italic bold'
            )
            self.btn_optimaze = Button(
                self.optimization_block,
                text=LANGUAGE[self.language]['btn_optimaze'],
                command=self.optimize_id,
                cursor='hand1'
            ).place(y=15, relx=.94, anchor='c')
            self.btn_optimaze_copy = Button(
                self.optimization_block,
                text=LANGUAGE[self.language]['btn_optimaze_copy'],
                command=self.copy_optimaze,
                cursor='hand1'
            ).place(y=35, x=1)
            Label(
                self.optimization_block,
                text=LANGUAGE[self.language]['lab_shortcat_id'],
                font=('Times New Roman', 10),
                foreground='red'
            ).place(relx=.5, rely=.305, anchor='c')
            frame_optimize_1 = Frame(
                self.optimization_block,
                borderwidth=0.5,
                relief='solid'
            )
            frame_optimize_1.place(
                y=75, relx=.5,
                anchor='c',
                relwidth=.5,
                relheight=.22
            )
            Label(
                frame_optimize_1,
                font=('Times New Roman', 12, 'bold italic'),
                foreground='#FF9B75',
                text=LANGUAGE[self.language]['format_optimize']
            ).place(y=15, relx=.5, anchor="c")
            self.format_optimize_var = StringVar()
            self.format_optimize_var.set('')
            Radiobutton(
                frame_optimize_1,
                text=LANGUAGE[self.language]['format_optimize_1'],
                variable=self.format_optimize_var,
                value='https://vk.com/id',
                cursor='tcross'
            ).place(y=75, relx=.5, anchor='c')
            Radiobutton(
                frame_optimize_1,
                text=LANGUAGE[self.language]['format_optimize_4'],
                variable=self.format_optimize_var,
                value='',
                cursor='tcross'
            ).place(y=45, relx=.5, anchor='c')
            Radiobutton(
                frame_optimize_1,
                text=LANGUAGE[self.language]['format_optimize_3'],
                variable=self.format_optimize_var,
                value='id',
                cursor='tcross'
            ).place(y=45, relx=.2, anchor='c')
            Radiobutton(
                frame_optimize_1,
                text=LANGUAGE[self.language]['format_optimize_2'],
                variable=self.format_optimize_var,
                value='@id',
                cursor='tcross'
            ).place(y=45, relx=.8, anchor='c')
            self.id_text = Text(
                self.optimization_block,
                foreground='white',
                background='#232629'
            )
            self.id_text.place(x=5, rely=.335, relwidth=.99, relheight=.65)
            self.optimaze_flowhack_1 = Label(
                self.optimization_block,
                image=self.average_flowhack,
                cursor='heart'
            )
            self.optimaze_flowhack_1.bind(
                '<Button-1>',
                lambda no_matter: self.open_webbrowser(
                    'http://vk.com/id311966436'
                )
            )
            self.optimaze_flowhack_1.place(x=5, rely=.265)
            self.optimaze_flowhack_2 = Label(
                self.optimization_block,
                image=self.average_flowhack,
                cursor='heart'
            )
            self.optimaze_flowhack_2.bind(
                '<Button-1>',
                lambda no_matter: self.open_webbrowser(
                    'http://vk.com/id311966436'
                )
            )
            self.optimaze_flowhack_2.place(relx=.89, rely=.265)

        # Заполнение pas_generate_block
        Label(
            self.pas_generator_block,
            font=('Times New Roman', 15, 'bold italic'),
            text=LANGUAGE[self.language]['pas_generator_main_title']
        ).place(relx=.5, y=20, anchor='c')
        frame_pas_generat = Frame(
            self.pas_generator_block,
            borderwidth=0.5,
            relief='solid'
        )
        frame_pas_generat.place(
            relx=.5,
            rely=.3,
            anchor='c',
            relwidth=.9,
            relheight=.3
        )
        self.chk_pas_symbol = BooleanVar()
        self.chk_pas_symbol.set(bool(False))
        self.chk_pas_number = BooleanVar()
        self.chk_pas_number.set(bool(True))
        self.chk_pas_upper = BooleanVar()
        self.chk_pas_upper.set(bool(True))
        Checkbutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_symbols'],
            var=self.chk_pas_symbol,
            cursor='cross'
        ).place(relx=.05, rely=.1)
        Checkbutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_number'],
            var=self.chk_pas_number,
            cursor='cross'
        ).place(relx=.05, rely=.44)
        Checkbutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_upper'],
            var=self.chk_pas_number,
            cursor='cross'
        ).place(relx=.05, rely=.78)
        self.pas_generator_encrypt = StringVar()
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_sha1'],
            variable=self.pas_generator_encrypt,
            value='sha1',
            cursor='tcross'
        ).place(rely=.1, relx=.54)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_md5'],
            variable=self.pas_generator_encrypt,
            value='md5',
            cursor='tcross'
        ).place(rely=.1, relx=.62)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_sha224'],
            variable=self.pas_generator_encrypt,
            value='sha224',
            cursor='tcross'
        ).place(rely=.1, relx=.7)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_sha256'],
            variable=self.pas_generator_encrypt,
            value='sha256',
            cursor='tcross'
        ).place(rely=.1, relx=.8)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_sha384'],
            variable=self.pas_generator_encrypt,
            value='sha384',
            cursor='tcross'
        ).place(rely=.1, relx=.9)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_sha512'],
            variable=self.pas_generator_encrypt,
            value='sha512',
            cursor='tcross'
        ).place(rely=.44, relx=.54)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_blake2b'],
            variable=self.pas_generator_encrypt,
            value='blake2b',
            cursor='tcross'
        ).place(rely=.44, relx=.62)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_blake2s'],
            variable=self.pas_generator_encrypt,
            value='blake2s',
            cursor='tcross'
        ).place(rely=.44, relx=.7)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_sha3_384'],
            variable=self.pas_generator_encrypt,
            value='sha3_384',
            cursor='tcross'
        ).place(rely=.44, relx=.8)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_sha3_512'],
            variable=self.pas_generator_encrypt,
            value='sha3_512',
            cursor='tcross'
        ).place(rely=.44, relx=.9)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_shake_128'],
            variable=self.pas_generator_encrypt,
            value='shake_128',
            cursor='tcross'
        ).place(rely=.78, relx=.8)
        Radiobutton(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_shake_256'],
            variable=self.pas_generator_encrypt,
            value='shake_256',
            cursor='tcross'
        ).place(rely=.78, relx=.9)
        Label(
            frame_pas_generat,
            text=LANGUAGE[self.language]['pas_generator_count_symbols'],
            font=('Times New Roman', 12, 'bold italic')
        ).place(rely=.78, relx=.54)
        self.pas_generator_count = IntVar()
        self.pas_generator_count.set(8)
        Spinbox(
            frame_pas_generat,
            from_=5,
            to=20,
            textvariable=self.pas_generator_count,
            font=('Times New Roman', 12, 'bold italic'),
            foreground='black',
            state='readonly'
        ).place(relx=.7, rely=.72, relwidth=.05)
        Label(
            self.pas_generator_block,
            text=LANGUAGE[self.language]['pas_generator_result'],
            font=('Times New Roman', 12, 'bold italic')
        ).place(anchor='c', relx=.5, rely=.55)
        self.pas_generator_result = Text(
            self.pas_generator_block,
            state=DISABLED,
            font=('Times New Roman', 11, 'bold')
        ).place(anchor='c', relx=.5, rely=.62, relwidth=.6, height=25)
        Button(
            self.pas_generator_block,
            text=LANGUAGE[self.language]['pas_generator_copy']
        ).place(anchor='c', relx=.5, rely=.72)
        flowhack_pas_generate_1 = Label(
            self.pas_generator_block,
            image=self.max_flowhack
        )
        flowhack_pas_generate_1.bind(
            '<Button-1>',
            lambda no_matter: self.open_webbrowser(
                'http://vk.com/id311966436'
            )
        )
        flowhack_pas_generate_1.place(x=20, rely=.9)
        flowhack_pas_generate_2 = Label(
            self.pas_generator_block,
            image=self.max_flowhack
        )
        flowhack_pas_generate_2.bind(
            '<Button-1>',
            lambda no_matter: self.open_webbrowser(
                'http://vk.com/id311966436'
            )
        )
        flowhack_pas_generate_2.place(relx=.85, rely=.9)

        # !!!!!! BUILD_SETTINGS_BLOCK !!!!!!

        self.frame_optimization_1 = Frame(
            self.settings_block, borderwidth=2,
            relief='ridge'
        )
        self.frame_optimization_1.place(relwidth=.5, relheight=0.6)
        self.lab_set_1 = Label(
            self.frame_optimization_1,
            text=self.value_ONE[1]
        )
        self.lab_set_1['font'] = (self.value_ONE[2], 12, self.value_ONE[4])
        self.lab_set_1.place(y=20, relx=.5, anchor='c')
        Label(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['lab_set_name'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=50)
        self.input_name_1 = Entry(
            self.frame_optimization_1,
            font=(self.value_ONE[2], 12),
        )
        self.input_name_1.insert(END, self.value_ONE[1])
        self.input_name_1.place(y=50, relx=.2, relwidth=.6)
        Label(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['lab_set_font'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=100)
        self.input_font_1 = Combobox(
            self.frame_optimization_1,
            font=('Times New Roman', 12, 'bold italic'),
            state='readonly'
        )
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
        Checkbutton(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['input_set_bold'],
            var=self.chk_bold_1,
            cursor='cross'
        ).place(relx=.05, y=250)
        self.chk_italic_1 = BooleanVar()
        if 'italic' in self.value_ONE[4]:
            self.chk_italic_1.set(bool(True))
        else:
            self.chk_italic_1.set(bool(False))
        Checkbutton(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['input_set_italic'],
            var=self.chk_italic_1,
            cursor='cross'
        ).place(relx=.3, y=250)
        self.chk_underline_1 = BooleanVar()
        if 'underline' in self.value_ONE[4]:
            self.chk_underline_1.set(bool(True))
        else:
            self.chk_underline_1.set(bool(False))
        Checkbutton(
            self.frame_optimization_1,
            text=LANGUAGE[self.language]['input_set_underline'],
            var=self.chk_underline_1,
            cursor='cross'
        ).place(relx=.5, y=250)

        self.frame_optimization_2 = Frame(
            self.settings_block,
            borderwidth=2,
            relief='ridge'
        )
        self.frame_optimization_2.place(relx=0.5, relwidth=.5, relheight=0.6)
        self.lab_set_2 = Label(
            self.frame_optimization_2,
            text=self.value_TWO[1]
        )
        self.lab_set_2['font'] = (self.value_TWO[2], 12, self.value_TWO[4])
        self.lab_set_2.place(y=20, relx=.5, anchor='c')
        self.lab_set_2 = Label(
            self.frame_optimization_2,
            text=self.value_TWO[1]
        )
        self.lab_set_2['font'] = (self.value_TWO[2], 12, self.value_TWO[4])
        self.lab_set_2.place(y=20, relx=.5, anchor='c')
        Label(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['lab_set_name'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=50)
        self.input_name_2 = Entry(
            self.frame_optimization_2,
            font=(self.value_TWO[2], 12)
        )
        self.input_name_2.insert(END, self.value_TWO[1])
        self.input_name_2.place(y=50, relx=.2, relwidth=.6)
        self.lab_set_font_2 = Label(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['lab_set_font'],
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.05, y=100)
        self.input_font_2 = Combobox(
            self.frame_optimization_2,
            font=('Times New Roman', 12, 'bold italic'),
            state='readonly'
        )
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
        Checkbutton(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['input_set_bold'],
            var=self.chk_bold_2,
            cursor='cross'
        ).place(relx=.05, y=250)
        self.chk_italic_2 = BooleanVar()
        if 'italic' in self.value_TWO[4]:
            self.chk_italic_2.set(bool(True))
        else:
            self.chk_italic_2.set(bool(False))
        Checkbutton(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['input_set_italic'],
            var=self.chk_italic_2,
            cursor='cross'
        ).place(relx=.3, y=250)
        self.chk_underline_2 = BooleanVar()
        if 'underline' in self.value_TWO[4]:
            self.chk_underline_2.set(bool(True))
        else:
            self.chk_underline_2.set(bool(False))
        Checkbutton(
            self.frame_optimization_2,
            text=LANGUAGE[self.language]['input_set_underline'],
            var=self.chk_underline_2,
            cursor='cross'
        ).place(relx=.5, y=250)

        self.frame_optimization_3 = Frame(
            self.settings_block,
            borderwidth=2,
            relief='ridge'
        )
        self.frame_optimization_3.place(
            relx=.025,
            rely=.6,
            relwidth=.95,
            relheight=.2
        )
        self.chk_other_block = BooleanVar()
        self.chk_other_block.set(bool(self.start_other_block))
        Checkbutton(
            self.frame_optimization_3,
            text=LANGUAGE[self.language]['set_onoff_other_block'],
            var=self.chk_other_block,
            cursor='cross'
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
        self.set_ok = Button(
            self.settings_block,
            image=ok,
            command=self.completion_settings,
            cursor='hand1'
        ).place(relx=.5, rely=.95, anchor='c')

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
        self.btn_rep_upload = Button(
            self.report_block, image=browse,
            command=self.searh_report_file,
            cursor='hand1'
        ).place(relx=.95, y=2)
        self.text_rep = Text(
            self.report_block,
            font=('Times New Roman', 12),
            foreground='white',
            background='#232629'
        )
        self.text_rep.place(relx=.01, rely=.2, relheight=.785, relwidth=.982)
        self.lab_rep_text_vk = Label(
            self.report_block,
            font=('Times New Roman', 12, 'bold italic underline'),
            text=LANGUAGE[self.language]['lab_rep_text_vk']
        ).place(relx=.4, y=40)
        self.lab_rep_vk = Label(
            self.report_block, image=self.average_flowhack,
            cursor='heart'
        )
        self.lab_rep_vk.place(relx=.75, y=36)
        self.lab_rep_vk.bind(
            '<Button-1>',
            lambda no_matter: self.open_webbrowser(
                'http://vk.com/id311966436'
            )
        )
        self.btn_rep_send = Button(
            self.report_block,
            image=send,
            command=self.sent_email,
            cursor='hand1'
        ).place(relx=.951, y=51)
        self.lbl_set_flowhack_1 = Label(
            self.settings_block,
            image=self.max_flowhack,
            cursor='heart'
        )
        self.lbl_set_flowhack_1.bind(
            '<Button-1>',
            lambda no_matter: self.open_webbrowser('http://vk.com/id311966436')
        )
        self.lbl_set_flowhack_1.place(relx=.05, rely=.92)
        self.lbl_set_flowhack_2 = Label(
            self.settings_block,
            image=self.max_flowhack,
            cursor='heart'
        )
        self.lbl_set_flowhack_2.bind(
            '<Button-1>',
            lambda no_matter: self.open_webbrowser('http://vk.com/id311966436')
        )
        self.lbl_set_flowhack_2.place(relx=.81, rely=.92)

        # !!!!!! BUILD_HELP_BLOCK !!!!!!
        Label(
            self.help_block,
            font=('Times New Roman', 14, 'bold italic'),
            text=LANGUAGE[self.language]['HELP_TEXT'],
        ).place(relx=.5, rely=.5, anchor='c')
        Label(
            self.help_block,
            font=('Times New Roman', 11, 'bold italic'),
            text='Version: ' + VERSION
        ).place(relx=.5, rely=.97, anchor='c')
        self.btn_help_copy = Button(
            self.help_block,
            text=LANGUAGE[self.language]['HELP_SAIT'],
            cursor='heart',
            command=self.copy_help
        )
        self.btn_help_copy.place(anchor='c', relx=.5, rely=.65)
        flowhack_help_1 = Label(
            self.help_block,
            image=self.max_flowhack,
            cursor='heart'
        )
        flowhack_help_1.bind(
            '<Button-1>',
            lambda no_matter: self.open_webbrowser(
                'http://vk.com/id311966436'
            )
        )
        flowhack_help_1.place(x=20, rely=.9)
        flowhack_help_2 = Label(
            self.help_block,
            image=self.max_flowhack,
            cursor='heart'
        )
        flowhack_help_2.bind(
            '<Button-1>',
            lambda no_matter: self.open_webbrowser(
                'http://vk.com/id311966436'
            )
        )
        flowhack_help_2.place(relx=.85, rely=.9)

        self.completion_list(start_list=bool(False))
        self.Main_window.protocol("WM_DELETE_WINDOW", exit_ex)
        self.Main_window.mainloop()

    def Optimize_records(self):
        def completion_list():
            listbox_optimization.delete(0, END)
            self.cursor_sql.execute('SELECT * FROM optimaze')
            all_records = self.cursor_sql.fetchall()
            for record in all_records:
                listbox_optimization.insert(
                    0,
                    f'{record[0]} | ID:{record[1]} | '
                    f'Date:{record[2].split()[0]}'
                )

        def curselection():
            try:
                return str(listbox_optimization.get(
                    listbox_optimization.curselection()
                ).split()[0]
                           )
            except BaseException as error:
                if str(error) == 'bad listbox index "": must be active, ' \
                                 'anchor, end, @x,y, or a number':
                    showerror('Error', ERROR[self.language]['delete'])

        def delete_record():
            name_rec = curselection()
            if name_rec != None:
                self.cursor_sql.execute(
                    f'DELETE FROM optimaze WHERE name = "{name_rec}"'
                )
                self.connect_sql.commit()
                completion_list()

        def delete_all_records():
            self.cursor_sql.execute('DROP TABLE IF EXISTS optimaze')
            self.connect_sql.commit()
            self.sql_optimaze()
            completion_list()

        def delete_old_records():
            old_date = dt.now() - timedelta(days=15)
            self.cursor_sql.execute('SELECT * FROM optimaze')
            all_records = self.cursor_sql.fetchall()
            for record in all_records:
                if (dt.strptime(record[2], DATE_FORMAT) - old_date).days < 0:
                    self.cursor_sql.execute(
                        f'DELETE FROM optimaze WHERE name = "{record[0]}"'
                    )
                    self.connect_sql.commit()
            completion_list()

        self.optimizee_window = Toplevel(background='#424242')
        self.optimizee_window.title('list records')
        self.optimizee_window.geometry('500x700')
        x = (self.optimizee_window.winfo_screenwidth() -
             self.optimizee_window.winfo_reqwidth()) / 2
        y = (self.optimizee_window.winfo_screenheight() -
             self.optimizee_window.winfo_reqheight()) / 2
        self.optimizee_window.wm_geometry("+%d+%d" % (x - 140, y - 300))
        self.optimizee_window.resizable(width=False, height=False)
        self.optimizee_window.iconphoto(
            True,
            PhotoImage(file='settings/ico/ico_main.png')
        )

        frame_optimize_win_1 = Frame(
            self.optimizee_window,
            borderwidth=0.5,
            relief='solid'
        )
        frame_optimize_win_1.place(relwidth=1, height=35)
        Button(
            frame_optimize_win_1,
            image=self.trash,
            command=delete_record,
            cursor='hand1'
        ).pack(side='left', padx=2)
        Button(
            frame_optimize_win_1,
            text=LANGUAGE[self.language]['del_all_optimize'],
            command=delete_all_records,
            cursor='hand1'
        ).pack(side='left', padx=2)
        Button(
            frame_optimize_win_1,
            text=LANGUAGE[self.language]['del_old_optimize'],
            command=delete_old_records,
            cursor='hand1'
        ).pack(side='left', padx=2)

        listbox_optimization = Listbox(
            self.optimizee_window,
            cursor='dot',
            font=('Times New Roman', 11, 'italic'),
            selectbackground='#f3be81',
            foreground='white',
            background='#232629'
        )
        listbox_optimization.bind(
            '<Double-Button-1>',
            lambda no_matter: self.optimization_open(curselection())
        )
        listbox_optimization.place(y=36, relwidth=1, relheight=.945)
        completion_list()

        self.optimizee_window.mainloop()

    def Add_edit(self, doing, name_list, name_record=None):
        def apply():
            return self.text_addedit.configure(
                font=(
                    self.input_addedit_font.get(),
                    self.input_size_addedit.get()
                )
            )

        def save():
            name = self.input_addedit_name.get()
            font = self.input_addedit_font.get()
            size = self.input_size_addedit.get()
            text = self.text_addedit.get(1.0, END)
            try:
                if len(name) > 40:
                    raise NameError('Record too long')
                if not set(":;!*#¤&").isdisjoint(name):
                    raise NameError('unacceptable_symbols')

                if doing == 'EDIT':
                    self.cursor_sql.execute(
                        f'''UPDATE list_records
                        SET name = "{name}",
                        text = "{text}",
                        font = "{font}",
                        size = {size}
                        WHERE (name = "{name_record}") and 
                        (name_list = "{name_list}")'''
                    )
                else:
                    self.cursor_sql.execute(
                        f'''INSERT INTO list_records VALUES ("{name_list}",
                         "{name}",
                         "{text}",
                         "{font}",
                         {size},
                         "{self.date_add}")'''
                    )

                self.connect_sql.commit()
                self.Add_edit_window.destroy()
                self.completion_list()
            except BaseException as error:
                if str(error) == 'Record too long':
                    showerror('Error', ERROR[self.language]['addedit_name'])
                if str(error) == 'unacceptable_symbols':
                    showerror(
                        'Error',
                        ERROR[self.language]['unacceptable_symbols']
                    )

        if doing == 'ADD':
            self.date_add = dt.now().strftime(DATE_FORMAT)
            if name_list == 'ONE':
                text_main = f'{LANGUAGE[self.language]["lbl_add_main"]} ' \
                            f'<{self.value_ONE[1]}>'
            else:
                text_main = f'{LANGUAGE[self.language]["lbl_add_main"]}' \
                            f' <{self.value_TWO[1]}>'
        else:
            text_main = f'{LANGUAGE[self.language]["lbl_edit_main"]} ' \
                        f'<{self.value_ONE[1]}>'
            self.cursor_sql.execute(
                f'''SELECT * FROM list_records 
                WHERE (name_list = "{name_list}") and 
                (name = "{name_record}")'''
            )
            addedit_all = self.cursor_sql.fetchone()

        self.Add_edit_window = Toplevel(background='#424242')
        self.Add_edit_window.title('Add_or_Edit')
        self.Add_edit_window.geometry('1200x950')
        x = (self.Add_edit_window.winfo_screenwidth() -
             self.Add_edit_window.winfo_reqwidth()) / 4
        y = (self.Add_edit_window.winfo_screenheight() -
             self.Add_edit_window.winfo_reqheight()) / 4
        self.Add_edit_window.wm_geometry("+%d+%d" % (x - 50, y - 180))
        self.Add_edit_window.bind(
            '<Control-Key-s>',
            lambda no_matter: save()
        )
        self.Add_edit_window.iconphoto(
            True,
            PhotoImage(file='settings/ico/ico_main.png')
        )

        frame = Frame(self.Add_edit_window, borderwidth=0.5, relief='solid')
        frame.place(relwidth=1, height=120)

        Label(
            self.Add_edit_window,
            text=text_main,
            font=('Times New Roman', 13, 'bold italic')
        ).place(relx=.5, y=20, anchor='c')
        label_flowhack_1 = Label(
            self.Add_edit_window,
            image=self.average_flowhack, cursor='heart'
        )
        label_flowhack_1.bind(
            '<Button-1>',
            lambda no_matter: self.open_webbrowser('http://vk.com/id311966436')
        )
        label_flowhack_1.place(relx=.1, anchor='c', y=20)
        label_flowhack_2 = Label(
            self.Add_edit_window,
            image=self.average_flowhack,
            cursor='heart'
        )
        label_flowhack_2.bind(
            '<Button-1>',
            lambda no_matter: self.open_webbrowser('http://vk.com/id311966436')
        )
        label_flowhack_2.place(relx=.9, anchor='c', y=20)
        Label(
            self.Add_edit_window,
            text=LANGUAGE[self.language]['lab_addedit_name'],
            font=('Times New Roman', 12, 'bold italic')
        ).place(x=10, y=50)
        self.input_addedit_name = Entry(
            self.Add_edit_window,
            font=('Times New Roman', 11, 'bold italic')
        )
        if doing == 'EDIT':
            self.input_addedit_name.insert(END, addedit_all[1])
        self.input_addedit_name.place(x=90, y=50, relwidth=.25, height=23)
        if doing == 'EDIT':
            Label(
                self.Add_edit_window,
                text=addedit_all[5],
                font=('Times New Roman', 12, 'bold italic')
            ).place(x=10, y=90)
        else:
            Label(
                self.Add_edit_window,
                text=self.date_add,
                font=('Times New Roman', 12, 'bold italic')
            ).place(x=10, y=90)
        Label(
            self.Add_edit_window,
            text=LANGUAGE[self.language]['lab_addedit_font'],
            font=('Times New Roman', 12, 'bold italic'),
        ).place(relx=.7, y=50)
        self.input_addedit_font = Combobox(
            self.Add_edit_window,
            font=('Times New Roman', 12, 'bold italic'),
            state='readonly'
        )
        if doing == 'EDIT':
            self.input_addedit_font.set(addedit_all[3])
        else:
            self.input_addedit_font.set('Arial')
        self.input_addedit_font['values'] = FONT
        self.input_addedit_font.place(relx=.76, y=50, relwidth=.2, height=23)
        Label(
            self.Add_edit_window,
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

        Button(
            self.Add_edit_window,
            text=LANGUAGE[self.language]['btn_addedit_apply'],
            command=lambda: apply(),
            cursor='hand1'
        ).place(relx=.5, y=60, anchor='c')
        Button(
            self.Add_edit_window,
            text=LANGUAGE[self.language]['btn_addedit_save'],
            command=lambda: save(),
            cursor='hand1'
        ).place(relx=.5, y=100, anchor='c')

        self.Add_edit_window.mainloop()


while start:
    App = Build()
