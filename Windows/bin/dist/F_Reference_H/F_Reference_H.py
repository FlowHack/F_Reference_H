from datetime import datetime as dt
from datetime import timedelta
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import (blake2b, blake2s, md5, sha1, sha3_384, sha3_512, sha224,
                     sha256, sha384, sha512, shake_128, shake_256)
from io import BytesIO
from mimetypes import guess_type
from os import getcwd, listdir, mkdir, path
from os.path import exists, isfile
from random import choice
from smtplib import SMTP_SSL, SMTPAuthenticationError
from sqlite3 import connect
from sys import exit as exit_ex
from time import sleep
from tkinter import (DISABLED, END, NORMAL, WORD, BooleanVar, IntVar, Listbox,
                     PhotoImage, StringVar, Text, Toplevel)
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesnocancel, showerror
from tkinter.ttk import (Button, Checkbutton, Combobox, Entry, Frame, Label,
                         Notebook, Radiobutton, Scrollbar, Spinbox)
from webbrowser import open as webopen

from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from urllib.request import urlretrieve

start: bool = True
SAIT = 'https://flowhack.github.io/'
VK = 'http://vk.com/id311966436'
VERSION = '1'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
ICO = ['add_file.png', 'average_flowhack.png', 'browse.png', 'eyeclose.png',
       'eyeopen.png', 'help.png', 'ico_main.png', 'main.ico',
       'max_flowhack.png', 'mini_flowhack.png', 'move.png', 'ok.png',
       'send.png', 'trash.png', 'update.png']
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
        'HELP_TEXT': 'Всю необходимую помощь Вы можете найти на сайте https://flowhack.github.io/\nПо использованию программы, дополнительным функциям, горячим клавишам, лицензионному соглашению и т.д.',
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
        'pas_generator_copy': 'Скопировать пароль',
        'pas_generator_create': 'Сгенерировать',
        'pas_generator_reset': 'Сбросить',
        'add_edit_exit_or_no': 'Мы заметили, что вы не сохранили данные! \n\nЖелаете сохранить данные?',
        'help_license': 'Используя программу Вы даёте разрешение на обработку пресональных данных и \nВы соглашаетесь с условиями лицензионного соглашения',
        'download_ico': 'Мы не нашли некоторых иконок в папке программы! Сейчас они будут установлены, для этого нам нужен будет интернет!',
    },
    'English': {
        'main_block': 'Home',
        'other_block': 'Other',
        'settings_block': 'Settings',
        'report_block': 'Feedback',
        'optimization_block': 'ID optimization',
        'previously_created': 'Previously created',
        'label_opt_main': 'Enter your IDs in the field',
        'btn_optimaze': 'Optimize',
        'lab_shortcat_id': 'Keyboard shortcuts may not work on Russian layout (<Ctrl A> - Select All, <Ctrl C> - Copy, <Ctrl X> - Cut, <Ctrl V> - Paste)',
        'lab_set_name': 'Name',
        'lab_set_font': 'Font',
        'lab_set_size': 'The size',
        'input_set_bold': 'Fatty',
        'input_set_italic': 'Italics',
        'input_set_underline': 'Underline',
        'set_onoff_other_block': 'Enable block "Other"',
        'set_language': 'Program language',
        'lab_rep_email': 'Email',
        'lab_rep_pas': 'Password',
        'lab_rep_addfile': 'Attach. file',
        'lab_input_rep_addfile': 'Select the file by clicking on the button ==>',
        'lab_rep_text_vk': 'You can write to me on Vkontakte, click ==>',
        'lbl_help_sait': 'You can open help for the program on the website, click ==>',
        'lbl_add_main': 'Adding a record to a block',
        'lbl_edit_main': 'Editing a block record',
        'lab_addedit_name': 'Name',
        'lab_addedit_font': 'Font',
        'lab_addedit_size': 'The size',
        'btn_addedit_apply': 'Apply to text',
        'btn_addedit_save': 'Save',
        'send_email_great': 'All perfectly! Message sent!',
        'send_email_wait': 'If this message is not sent within 5-15 seconds, then an error has occurred!',
        'label_opt_main_id': 'It turned out in total: ',
        'btn_optimaze_copy': 'Copy field',
        'format_optimize_1': 'https://vk.com/id+value',
        'format_optimize_2': '@id+value',
        'format_optimize_3': 'id+value',
        'format_optimize_4': 'value',
        'format_optimize': 'Output formats',
        'optimizee_name': 'Name',
        'optimizee_date': 'Date of creation',
        'del_old_optimize': 'Delete old entries',
        'del_all_optimize': 'Delete all entries',
        'HELP_TEXT': 'All the help you need can be found at https://flowhack.github.io/\nOn using the program, additional functions, hotkeys, license agreement, etc.',
        'HELP_SAIT': 'Copy link',
        'pas_generator_block': 'Password generator',
        'pas_generator_main_title': "Let's generate a password!",
        'pas_generator_result': 'Your password:',
        'pas_generator_count_symbols': 'Characters',
        'pas_generator_symbols': 'Use additional sivols',
        'pas_generator_number': 'Use numbers',
        'pas_generator_upper': 'Use capital letters',
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
        'pas_generator_copy': 'Copy password',
        'pas_generator_create': 'Generate',
        'pas_generator_reset': 'Reset',
        'add_edit_exit_or_no': 'We noticed that you have not saved your data!\n\nDo you want to save your data?',
        'help_license': 'By using the program you give permission to process personal data and \n You agree to the terms of the license agreement',
        'download_ico': "We didn't find some icons in the program folder! Now they will be installed, for this we need the Internet!",
    },
    'French': {
        'main_block': 'Domicile',
        'other_block': 'Autre',
        'settings_block': 'Réglages',
        'report_block': "Retour d'information",
        'optimization_block': 'Optimisation des identifiants',
        'previously_created': 'Créée précédemment',
        'label_opt_main': 'Entrez vos identifiants dans le champ',
        'btn_optimaze': 'Optimiser',
        'lab_shortcat_id': 'Les raccourcis clavier peuvent ne pas fonctionner sur la disposition russe (<Ctrl A> - Tout sélectionner, <Ctrl C> - Copier, <Ctrl X> - Couper, <Ctrl V> - Coller)',
        'lab_set_name': 'Nom',
        'lab_set_font': 'Caractère',
        'lab_set_size': 'La taille',
        'input_set_bold': 'Gras',
        'input_set_italic': 'Italique',
        'input_set_underline': 'Souligner',
        'set_onoff_other_block': 'Activer le bloc "Autre"',
        'set_language': 'Langue du programme',
        'lab_rep_email': 'Email',
        'lab_rep_pas': 'Mot de passe',
        'lab_rep_addfile': 'Attacher. fichier',
        'lab_input_rep_addfile': 'Sélectionnez un fichier en cliquant sur le bouton ==>',
        'lab_rep_text_vk': "Vous pouvez m'écrire sur Vkontakte, cliquez sur ==>",
        'lbl_help_sait': "Vous pouvez ouvrir l'aide du programme sur le site Web, cliquez sur ==>",
        'lbl_add_main': 'Ajouter un enregistrement à un bloc',
        'lbl_edit_main': "Modification d'un enregistrement de bloc",
        'lab_addedit_name': 'Nom',
        'lab_addedit_font': 'Caractère',
        'lab_addedit_size': 'La taille',
        'btn_addedit_apply': 'Appliquer au texte',
        'btn_addedit_save': 'Sauvegarder',
        'send_email_great': 'Tout parfaitement! Message envoyé!',
        'send_email_wait': "Si ce message n'est pas envoyé dans les 5 à 15 secondes, une erreur s'est produite!",
        'label_opt_main_id': "Il s'est avéré au total: ",
        'btn_optimaze_copy': 'Copier le champ',
        'format_optimize_1': 'https://vk.com/id+valeur',
        'format_optimize_2': '@id+valeur',
        'format_optimize_3': 'id+valeur',
        'format_optimize_4': 'valeur',
        'format_optimize': 'Formats de sortie',
        'optimizee_name': 'Nom',
        'optimizee_date': 'Date de création',
        'del_old_optimize': 'Supprimer les anciennes entrées',
        'del_all_optimize': 'Supprimer toutes les entrées',
        'HELP_TEXT': "Toute l'aide dont vous avez besoin est disponible sur https://flowhack.github.io/\nUtilisation du programme, des fonctions supplémentaires, des raccourcis clavier, du contrat de licence, etc.",
        'HELP_SAIT': 'Copier le lien',
        'pas_generator_block': 'Générateur de mot de passe',
        'pas_generator_main_title': 'Générons un mot de passe!',
        'pas_generator_result': 'Votre mot de passe:',
        'pas_generator_count_symbols': 'Personnages',
        'pas_generator_symbols': 'Utiliser des sivols supplémentaires',
        'pas_generator_number': 'Utilisez des nombres',
        'pas_generator_upper': 'Utiliser des lettres majuscules',
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
        'pas_generator_copy': 'Copier le mot de passe',
        'pas_generator_create': 'Produire',
        'pas_generator_reset': 'Réinitialiser',
        'add_edit_exit_or_no': "Nous avons remarqué que vous n'avez pas enregistré vos données! \n\nVoulez-vous sauvegarder vos données?",
        'help_license': 'En utilisant le programme, vous autorisez le traitement des données personnelles et \nVous acceptez les termes du contrat de licence',
        'download_ico': "Nous n'avons pas trouvé d'icônes dans le dossier du programme! Maintenant, ils seront installés, pour cela nous avons besoin d'Internet!",
    }
}
ERROR = {
    'Russian': {
        'delete': 'Произошла непредвиденная ошибка!\n\nВы не выбрали запись!',
        'addedit_name': 'Похоже, что длина введеного вами имени документа длиннее 40 сиволов!\n\nИсправьте эту ошибку! <Краткость - сестра таланта>',
        'settings_title_ONE': 'Похоже, что длина введеного вами имени в первом документе длиннее 40 сиволов!\n\nИсправьте эту ошибку! <Краткость - сестра таланта>',
        'settings_title_TWO': 'Похоже, что длина введеного вами имени во втором документе длиннее 40 сиволов!\n\nИсправьте эту ошибку! <Краткость - сестра таланта>',
        'settings_title_is_empty_ONE': 'Похоже, что вы ввели пустую строку в навзании первого документа!\n\nИсправьте эту ошибку! А то что-то слишком пусто получается :)',
        'settings_title_is_empty_TWO': 'Похоже, что вы ввели пустую строку в названии второго документа!\n\nИсправьте эту ошибку!',
        'report_gmail': 'Неправильный логин или пароль!\n\nМы заметили, что вы отправляете сообщение с почты @gmail.com, возможно у вас запрещена отправка из неизвестных источников,тогда для решения проблемы перейдите по ссылке, которую мы сейчас добавили в текстовое поле, и включите функцию отправки сообщений из неизвестных источников! Также вы можете использовать просто другую почту.\n\nВнимание! После отправки сообщения обязательно выключите функцию на сайте! Мы не несём ответственность за совершенные вами действия!',
        'report_connect': 'Произошла непредвиденная ошибка!\n\nПожалуйста, проверьте ваше подключение к сети, перезапустите программу. Если не получается исправить ошибку, то напишите об ошибке в соостветствующей вкладке приложения, мы поможем :)\n\nЕсли не получается исправить ошибку, то напишите об ошибке в соостветствующей вкладке приложения, мы поможем :)',
        'report_title_addr_is_empty': 'Вы не заполнили поле EMAIL!\n\nЗаполните его, оно обязательно)',
        'report_password_is_empty': 'Вы не заполнили поле Пароль!\n\nЗаполните его, оно обязательно)',
        'report_message_is_empty': 'Вы не написали сообщение! Оно для вас шутка?\n\nЗаполните его, оно обязательно)',
        'report_time': 'В целях безопасности мы запретили отправлять сообщения чаше, чем 1 раз в час.\n\nМожете написать через {time_ost:0.0f} мин.',
        'report_message_too_short': 'Вы написали слишком короткое сообщение, врятли вы смогли хорошо в нём изложить свою мысль!\n\nИзложите её развёрнуто, не менее 30 символов! Нам ещё надо это понять и исправить!',
        'unacceptable_symbols': 'Вы использовали недопустимые символы! (:;!*#¤&)',
        'not_name': 'Извините, но название "name" нельзя использовать!',
        'not_text': 'Извините, но содержимое текста нельяз называть просто "text!',
        'text_null': 'Поле текста пустое! Так нельзя!',
        'name_null': 'Поле названия пустое! Так нельзя!',
        'unacceptable_symbols_ONE': 'Вы использовали недопустимые символы в названии первого блока! (:;!*#¤&)',
        'unacceptable_symbols_TWO': 'Вы использовали недопустимые символы в названии второго блока! (:;!*#¤&)',
        'download_ico_internet': f'Произошла непредвиденная ошибка!\n\nВозможно у вас выключен интернет! У нас не получается скачать нужные файлы, поэтому мы вынуждены отменить запуск программы.\n\nЕсли не получается решить проблему, то на сайте {SAIT} скачайте программу архивом!',
    },
    'Englsh': {
        'delete': 'An unexpected error has occurred!\n\nYou have not selected an entry!',
        'addedit_name': 'It looks like the document name you entered is longer than 40 symbols!\n\nCorrect this error! <Brevity is the sister of talent>',
        'settings_title_ONE': 'It looks like the name you entered in the first document is longer than 40 symbols!\n\nCorrect this error! <Brevity is the sister of talent>',
        'settings_title_TWO': 'It looks like the length of the name you entered in the second document is longer than 40 symbols!\n\nCorrect this error! <Brevity is the sister of talent>',
        'settings_title_is_empty_ONE': 'It looks like you entered an empty line in the title of the first document!\n\nCorrect this error! And then something turns out too empty :)',
        'settings_title_is_empty_TWO': 'It looks like you entered a blank line in the title of the second document!\n\nCorrect this error!',
        'report_gmail': 'Incorrect login or password!\n\nWe noticed that you are sending a message from @ gmail.com mail, perhaps you are prohibited from sending from unknown sources, then to solve the problem, follow the link that we have now added to the text field and enable the function of sending messages from unknown sources! You can also use just another mail.\n\nAttention! After sending the message, be sure to turn off the function on the site! We are not responsible for your actions!',
        'report_connect': "An unexpected error has occurred!\n\nPlease check your network connection, restart the program. If you can't fix the error, then write about the error in the appropriate tab of the application, we will help :)\n\nIf you can't fix the error, then write about the error in the appropriate tab of the application, we will help :)",
        'report_title_addr_is_empty': "You have not filled out the EMAIL field!\n\nFill it in, it's required)",
        'report_password_is_empty': "You have not filled in the Password field!\n\nFill it in, it's required)",
        'report_message_is_empty': "You didn't write a message! Is it a joke to you?\n\nFill it in, it's required)",
        'report_time': 'For security reasons, we have prohibited sending messages more often than 1 time per hour.\n\nYou can write through {time_ost:0.0f} min.',
        'report_message_too_short': 'You wrote too short a message, vryatli you were able to express your thought well in it!\n\nState it in detail, at least 30 characters! We still need to understand and fix this!',
        'unacceptable_symbols': 'You have used invalid characters! (:;!*#¤&)',
        'not_name': 'Sorry, but "name" cannot be used!',
        'not_text': "Sorry, but you can't just call the text content 'text!'",
        'text_null': 'The text field is empty! You can not do it this way!',
        'name_null': 'The title field is empty! You can not do it this way!',
        'unacceptable_symbols_ONE': 'You have used invalid characters in the name of the first block! (:;!*#¤&)',
        'unacceptable_symbols_TWO': 'You have used invalid characters in the name of the second block! (:;!*#¤&)',
        'download_ico_internet': f"An unexpected error has occurred!\n\nPerhaps your Internet is turned off! We can't download the files we need, so we have to cancel the launch of the program.\n\nIf you cannot solve the problem, then download the program from the {SAIT} website in an archive!",
    },
    'French': {
        'delete': "Une erreur inattendue est survenue!\n\nVous n'avez sélectionné aucune entrée!",
        'addedit_name': "Il semble que le nom du document que vous avez entré compte plus de 40 symboles!\n\nCorrigez cette erreur! <La brièveté est la sœur du talent>",
        'settings_title_ONE': "Il semble que le nom que vous avez entré dans le premier document compte plus de 40 symboles!\n\nИcorrige cette erreur! <La brièveté est la sœur du talent>",
        'settings_title_TWO': "Il semble que la longueur du nom que vous avez entré dans le deuxième document dépasse 40 symboles!\n\nCorrigez cette erreur! <La brièveté est la sœur du talent>",
        'settings_title_is_empty_ONE': "Il semble que vous ayez entré une ligne vide dans le titre du premier document!\n\nCorrigez cette erreur!Et puis quelque chose s'avère trop vide :)",
        'settings_title_is_empty_TWO': 'Il semble que vous ayez entré une ligne vide dans le titre du deuxième document!\n\nCorrigez cette erreur!',
        'report_gmail': "Identifiant ou mot de passe incorrect!\n\nNous avons remarqué que vous envoyez un message depuis @ gmail.com, il vous est peut-être interdit d'envoyer à partir de sources inconnues, alors pour résoudre le problème, suivez le lien que nous avons maintenant ajouté dans le champ de texte et activez la fonction d'envoi de messages à partir de sources inconnues! Vous pouvez également utiliser juste un autre courrier.\n\nAttention! Après avoir envoyé le message, assurez-vous de désactiver la fonction sur le site! Nous ne sommes pas responsables de vos actions!",
        'report_connect': "Une erreur inattendue est survenue!\n\nVeuillez vérifier votre connexion réseau, redémarrez le programme. Si vous ne pouvez pas corriger l'erreur, écrivez sur l'erreur dans l'onglet approprié de l'application, nous vous aiderons :)\n\nSi vous ne pouvez pas corriger l'erreur, écrivez sur l'erreur dans l'onglet approprié de l'application, nous vous aiderons :)",
        'report_title_addr_is_empty': "Vous n'avez pas rempli le champ EMAIL!\n\nRemplissez-le, c'est obligatoire)",
        'report_password_is_empty': "Vous n'avez pas rempli le champ Mot de passe!\n\ncRemplissez-le, c'est obligatoire)",
        'report_message_is_empty': "Vous n'avez pas écrit de message! Est-ce une blague pour vous?\n\ncRemplissez-le, c'est obligatoire)",
        'report_time': "Pour des raisons de sécurité, nous avons interdit l'envoi de messages plus d'une fois par heure.\n\nVous pouvez écrire en {time_ost: 0.0f} minutes.",
        'report_message_too_short': 'Vous avez écrit un message trop court, vryatli vous avez bien pu y exprimer votre pensée!\n\nDites-le en détail, au moins 30 caractères! Nous devons encore comprendre et résoudre ce problème!',
        'unacceptable_symbols': 'Vous avez utilisé des caractères invalides! (:;!*#¤&)',
        'not_name': 'Désolé, mais "nom" ne peut pas être utilisé!',
        'not_text': 'Désolé, mais vous ne pouvez pas simplement appeler le contenu du texte "texte!"',
        'text_null': 'Le champ de texte est vide! Vous ne pouvez pas le faire de cette façon!',
        'name_null': 'cLe champ de titre est vide! Vous ne pouvez pas le faire de cette façon!',
        'unacceptable_symbols_ONE': 'Vous avez utilisé des caractères invalides dans le nom du premier bloc! (:;!*#¤&)',
        'unacceptable_symbols_TWO': 'Vous avez utilisé des caractères invalides dans le nom du deuxième bloc! (:;!*#¤&)',
        'download_ico_internet': f"Une erreur inattendue est survenue!\n\nPeut-être que votre Internet est désactivé! Nous ne pouvons pas télécharger les fichiers dont nous avons besoin, nous devons donc annuler le lancement du programme.\n\nSi vous ne parvenez pas à résoudre le problème, téléchargez le programme depuis le site Web {SAIT} dans une archive!",
    }
}
LANGUAGE_LIST = ['Russian', 'English', 'French']
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

        # Create folder ico
        if 'ico' in listdir(self.path_settings):
            self.path_ico = f'{self.path_settings}/ico'
        else:
            mkdir(f'{self.path_settings}/ico')
            self.path_ico = f'{self.path_settings}/ico'

    def download_page(self):
        def download_ico(name):
            try:
                url_name = f'{self.path_ico}/{name}'
                urlretrieve(SAIT + 'download/png/' + name, url_name)
            except BaseException as error:
                if str(error) == '<urlopen error [Errno -3] Temporary ' \
                                 'failure in name resolution>':
                    showerror(
                        'Error',
                        ERROR[self.language]['download_ico_internet']
                    )
                    exit_ex()

        schet = 0

        for number in range(len(ICO)):
            if ICO[number] not in listdir(self.path_ico):
                schet = 1

        if schet == 1:
            showerror('Error', LANGUAGE[self.language]['download_ico'])
            for number in range(len(ICO)):
                download_ico(ICO[number])

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
            main_name TEXT NOT NULL,
            name TEXT NOT NULL,
            font TEXT NOT NULL,
            size INT NOT NULL,
            bolds TEXT NOT NULL,
            italics TEXT NOT NULL,
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
            name_list TEXT NOT NULL,
            name TEXT NOT NULL,
            text TEXT NOT NULL,
            font TEXT NOT NULL,
            size INT NOT NULL,
            date TEXT NOT NULL)'''
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
            turn_out INT NOT NULL,
            date TEXT NOT NULL,
            text TEXT NOT NULL)'''
        )
        self.connect_sql.commit()

    def sql_settings(self):
        date = dt.now()

        self.cursor_sql.execute(
            '''CREATE TABLE IF NOT EXISTS settings(
            other_block BOOLEAN NOT NULL,
            launch BOOLEAN NOT NULL,
            language TEXT NOT NULL,
            send_email TEXT NOT NULL)'''
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
        self.list_block_1.delete(0, END)
        self.list_block_2.delete(0, END)

        if start_list:
            self.list_record_ONE, self.list_record_TWO = \
                self.create_value_records()

        counter = 1
        for record in self.list_record_ONE:
            self.list_block_1.insert(END, f' {counter}: {record[1]}')
            counter += 1

        counter = 1
        for record in self.list_record_TWO:
            self.list_block_2.insert(END, f' {counter}: {record[1]}')
            counter += 1

    def copy_optimaze(self):
        self.id_text.clipboard_clear()
        self.id_text.clipboard_append(self.id_text.get(1.0, END))

    def copy_help(self):
        self.btn_help_copy.clipboard_clear()
        self.btn_help_copy.clipboard_append('https://flowhack.github.io/')

    def copy_generate_password(self):
        password = self.pas_generator_result.get()
        self.pas_generator_result.clipboard_clear()
        self.pas_generator_result.clipboard_append(password)

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

        title_ONE, title_TWO = self.input_name_1.get().lstrip().rstrip(), self.input_name_2.get().lstrip().rstrip()
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
            if (title_ONE == '') or (title_ONE == ' '):
                raise NameError('Empty string in the first')
            if (title_TWO == '') or (title_TWO == ' '):
                raise NameError('Empty string in the second')
            if not set(":;!*#¤&").isdisjoint(title_ONE):
                raise NameError('unacceptable_symbols_ONE')
            if not set(":;!*#¤&").isdisjoint(title_TWO):
                raise NameError('unacceptable_symbols_TWO')

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
                WHERE main_name = "TWO"'''
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
            if str(error) == 'unacceptable_symbols_ONE':
                showerror('Error',
                          ERROR[self.language]['unacceptable_symbols_ONE'])
            if str(error) == 'unacceptable_symbols_TWO':
                showerror('Error',
                          ERROR[self.language]['unacceptable_symbols_TWO'])

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

    def password_generator_reset(self):
        self.pas_generator_result.configure(state=NORMAL)
        self.pas_generator_result.delete(0, END)
        self.pas_generator_result.configure(state=DISABLED)
        self.pas_generator_encrypt.set('')
        self.pas_generator_count.set(8)
        self.chk_pas_symbol.set(bool(False))
        self.chk_pas_number.set(bool(True))
        self.chk_pas_upper.set(bool(True))

    def password_generate(self):
        password = ''
        self.pas_generator_result.configure(state=NORMAL)
        self.pas_generator_result.delete(0, END)
        self.pas_generator_result.configure(state=DISABLED)
        main_list_symbols: list = ['a', 'b', 'c', 'd', 'i', 'f', 'g', 'h',
                                   'i', 'g', 'k', 'l', 'm', 'n', 'o', 'p',
                                   'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                                   'y', 'z']
        additional_symbols: list = ['!', '.', ',', '@', '#', '$', '%', '?']
        number_symbols: list = ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                '9']
        upper_symbols: list = ['A', 'B', 'C', 'D', 'I', 'F', 'G', 'H', 'I',
                               'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        if self.chk_pas_symbol.get():
            main_list_symbols += additional_symbols
        if self.chk_pas_number.get():
            main_list_symbols += number_symbols
        if self.chk_pas_upper.get():
            main_list_symbols += upper_symbols

        number_in_password = self.pas_generator_count.get()

        for char in range(number_in_password):
            password += choice(main_list_symbols)

        if self.pas_generator_encrypt.get() == 'sha1':
            password = sha1(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'md5':
            password = md5(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'sha224':
            password = sha224(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'sha256':
            password = sha256(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'sha384':
            password = sha384(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'sha512':
            password = sha512(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'blake2b':
            password = blake2b(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'blake2s':
            password = blake2s(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'sha3_384':
            password = sha3_384(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'sha3_512':
            password = sha3_512(password.encode('utf-8')).hexdigest()
        if self.pas_generator_encrypt.get() == 'shake_128':
            password = shake_128(password.encode('utf-8')).hexdigest(255)
        if self.pas_generator_encrypt.get() == 'shake_256':
            password = shake_256(password.encode('utf-8')).hexdigest(255)

        self.pas_generator_result.configure(state=NORMAL)
        self.pas_generator_result.insert(END, password)
        self.pas_generator_result.configure(state=DISABLED)
        btn_copy = Button(
            self.pas_generator_block,
            text=LANGUAGE[self.language]['pas_generator_copy'],
            command=self.copy_generate_password,
            cursor='based_arrow_down'
        )
        btn_copy.place(anchor='c', relx=.5, rely=.84)
        btn_copy.after(10000, btn_copy.destroy)


class Splash(Toplevel):
    def __init__(self):
        Toplevel.__init__(self, background='#DF9953', cursor='heart')
        self.overrideredirect(1)
        self.geometry('600x600')
        x = (self.winfo_screenwidth() -
             self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() -
             self.winfo_reqheight()) / 2
        self.wm_geometry("+%d+%d" % (x - 200, y - 200))
        img = Image.open(BytesIO(
            b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44'
            b'\x52\x00\x00\x01\x00\x00\x00\x01\x00\x08\x06\x00\x00\x00\x5c'
            b'\x72\xa8\x66\x00\x00\x00\x04\x67\x41\x4d\x41\x00\x00\xb1\x8f'
            b'\x0b\xfc\x61\x05\x00\x00\x00\x01\x73\x52\x47\x42\x00\xae\xce'
            b'\x1c\xe9\x00\x00\x00\x20\x63\x48\x52\x4d\x00\x00\x7a\x26\x00'
            b'\x00\x80\x84\x00\x00\xfa\x00\x00\x00\x80\xe8\x00\x00\x75\x30'
            b'\x00\x00\xea\x60\x00\x00\x3a\x98\x00\x00\x17\x70\x9c\xba\x51'
            b'\x3c\x00\x00\x00\x06\x62\x4b\x47\x44\x00\xff\x00\xff\x00\xff'
            b'\xa0\xbd\xa7\x93\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x00'
            b'\x9d\x00\x00\x00\x9d\x01\x8f\x72\xe7\x6e\x00\x00\x36\xd8\x49'
            b'\x44\x41\x54\x78\xda\xed\xbd\x79\x9c\x5c\x57\x79\xe7\xfd\x7d'
            b'\xce\xbd\xb5\x75\xf5\xae\xad\x25\xcb\xf2\x26\x5b\x5e\xb0\xc1'
            b'\x0b\xc6\x1b\x8b\xcd\xe6\x15\x06\x98\x49\x08\x86\x40\x20\x81'
            b'\x04\x78\x27\x6f\xb0\x24\x87\x25\x4c\x42\x32\x80\x2d\x7b\xf2'
            b'\x92\x00\x61\xf2\x21\xcc\xcb\x10\x08\x24\x19\x02\xc6\x96\x6c'
            b'\x6c\xb0\xc1\x18\xf0\x86\xf1\xbe\xca\x96\x64\xed\x4b\xef\xdd'
            b'\xb5\xdd\x7b\x9f\xf9\xe3\x54\xb5\x5a\x52\x77\xab\x97\xaa\xba'
            b'\x55\xdd\xe7\xfb\xf9\x94\x96\xee\x5a\xce\x3d\x75\xcf\xef\x3c'
            b'\xe7\x39\xcf\x79\x1e\xc1\xd1\x34\x5c\x7f\x2b\x88\x42\x64\x48'
            b'\xa9\xd0\x02\x64\x81\x45\xc0\xf2\xf2\x63\x19\xb0\xb8\xfc\xb3'
            b'\x6e\xa0\x03\x68\x07\x5a\x81\x4c\xf9\x91\x06\x7c\xc0\x00\x89'
            b'\xf2\x5b\x97\x80\x08\x08\x80\x3c\x90\x2b\x3f\x86\x80\xc1\xf2'
            b'\xa3\x17\xd8\x5f\x7e\xec\x05\x76\x01\x3b\xcb\x3f\x1f\x51\xc3'
            b'\x68\x94\xa0\x20\x11\xdc\xfc\xe6\xb8\x7b\xca\x31\x5d\x24\xee'
            b'\x06\x38\x8e\xe4\xf3\xbf\x82\x97\xb7\x40\x7b\x07\x7e\x04\x6d'
            b'\x08\x9d\x28\xc7\x02\x27\x02\x27\x01\xc7\x02\x2b\x81\x63\xb0'
            b'\x83\x3c\x85\x1d\xd8\x49\xec\xe0\xae\x25\x01\x50\xc4\x0a\x45'
            b'\x01\x18\x00\x76\x00\xdb\xcb\x8f\x6d\xc0\x4b\xc0\x16\x85\x5e'
            b'\x03\x43\x1d\x29\x8a\x23\x01\x7c\xfe\xad\x71\xf7\xac\xe3\x70'
            b'\x9c\x00\x34\x00\xeb\x36\x01\xe0\x01\xad\x28\x4b\x51\x4e\x43'
            b'\x38\x15\x38\x19\x58\x03\x1c\x0f\xb4\x01\x2d\xd8\x41\xde\xc8'
            b'\x04\xc0\x28\x30\x8c\x15\x84\x67\x80\xa7\x81\x27\x51\x9e\x41'
            b'\xd8\x1b\xc1\xb0\x40\x78\xd3\x95\x71\x37\xd5\xe1\x04\x20\x06'
            b'\xd6\xdd\x0a\x80\x87\xd0\x8e\xb0\x12\x78\x15\x70\x4e\xf9\xef'
            b'\xd5\x40\x17\x76\xb0\xcf\x97\xef\x47\xb1\xa2\xd0\x0b\xbc\x00'
            b'\x3c\x06\x3c\x0e\xfc\x06\xd8\xa2\x1e\x83\x44\x84\x37\x5d\x11'
            b'\x77\x33\x17\x1e\xf3\xe5\x06\x6b\x68\xae\xbb\x13\x0a\x59\xc8'
            b'\xf4\x93\xc1\x9a\xed\xe7\x02\xe7\x97\x1f\x27\x03\x9d\x58\x33'
            b'\x7e\x21\x51\x02\xfa\x80\x67\x81\x07\x81\xfb\xb1\x82\xb0\x33'
            b'\x80\x51\x03\xdc\xec\x2c\x84\x9a\xe3\x04\xa0\x46\xac\xdb\x88'
            b'\x9d\xf7\x84\x36\xe0\x14\xe0\x12\xe0\x62\xe0\xd5\x40\x0f\x76'
            b'\xcd\xee\x38\x48\x0e\xd8\x03\x3c\x0c\xdc\x0b\xfc\x02\x78\x9e'
            b'\x90\x21\x04\xdd\x70\x75\xdc\xcd\x9b\x9f\x38\x01\xa8\x22\xeb'
            b'\x6e\x07\xf5\xc1\x14\x69\x55\x38\x1d\xb8\x14\x78\x1d\x76\xc6'
            b'\x5f\x8c\x5d\xe7\x3b\x8e\x4e\x08\x1c\xc0\x2e\x15\x7e\x02\xfc'
            b'\x54\xe0\x19\xe3\x31\xa4\x8a\xde\x70\x79\xdc\xcd\x9b\x3f\x38'
            b'\x01\x98\x23\xff\xf4\x22\x3c\xfd\x14\x78\x86\x64\x64\xcd\xf9'
            b'\x37\x02\x6f\xc6\x9a\xf7\x8b\xb1\xdb\x6d\x8e\xd9\x13\x61\xc5'
            b'\xe0\x11\x60\x23\x70\x17\xca\x66\x3f\x20\x3f\x9a\x85\x2f\xbd'
            b'\x29\xee\xe6\x35\x37\x4e\x00\x66\xc9\x27\x6e\x87\x20\x81\xa4'
            b'\x0a\x2c\x05\x5e\x0f\x5c\x55\xfe\xfb\x18\x6a\xbf\x15\xb7\x50'
            b'\x09\xb0\xf1\x07\xf7\x02\x3f\x10\xe1\x5e\x63\xd8\x13\x45\xe8'
            b'\x8d\xce\x81\x38\x2b\x9c\x00\xcc\x90\xf5\xb7\x01\x90\x52\x61'
            b'\x0d\x70\x35\xf0\x36\xe0\x2c\x6c\x90\x8d\xa3\x7e\xe4\x80\xa7'
            b'\x80\x1f\x01\x3f\x22\xe2\x49\x84\xc2\x86\xab\xe2\x6e\x56\x73'
            b'\xe1\x04\x60\x1a\x5c\xbf\x11\xd2\x01\x8c\x26\x68\x47\x79\x0d'
            b'\xf0\x6e\xe0\x2d\xd8\xe8\x3b\xb7\xae\x8f\x97\x08\x6b\x15\xdc'
            b'\x01\xfc\xbb\xc2\x7d\x5d\x2d\x0c\x0e\xe6\xc1\xf9\x0a\x8e\x8e'
            b'\x13\x80\x29\x58\x77\x2b\x68\x04\xe2\xb1\x18\x78\x33\xc2\x7b'
            b'\x81\x8b\xb0\xdb\x76\x8e\xc6\x63\x00\xb8\x0f\xf8\xae\xc0\x1d'
            b'\x26\x64\x5f\x64\xd0\x1b\x9d\x55\x30\x29\x4e\x00\x26\x60\xfd'
            b'\x6d\xe0\x87\x48\xc9\xa7\x07\xb8\x06\xb8\x16\xbb\x7d\xe7\xcc'
            b'\xfc\xe6\x20\x8f\xdd\x4e\xfc\x16\x70\x4b\x08\xbb\x0d\xa8\x8b'
            b'\x3c\x3c\x12\x27\x00\xe3\x58\xbf\x11\x7c\x03\xa5\x90\x1e\x84'
            b'\xb7\x03\xef\xc7\x46\xe8\x2d\xb4\x20\x1d\x14\x30\x18\x7c\x2f'
            b'\x85\x11\xeb\xd3\x8c\x34\x20\x08\x0b\x44\x44\xcd\x72\xe3\x14'
            b'\xb1\xbb\x07\xdf\x42\xf9\x41\xc9\x63\xa7\x1f\x39\x21\x18\x4f'
            b'\x93\x7c\x8f\xb5\xe5\xba\x8d\x76\xca\x68\xb1\xa7\xe8\xae\x01'
            b'\xfe\x08\xbb\x77\xbf\xe0\x06\x3e\x80\x11\x9f\x8e\xf4\x31\x2c'
            b'\x6d\x3d\x8d\xf6\xd4\x0a\x52\x7e\x1b\x00\x85\x60\x98\xc1\xc2'
            b'\x0e\xf6\x0e\x3f\x4d\x7f\x7e\x07\xaa\x41\xdc\x4d\x9d\x2e\x15'
            b'\x21\xf8\xba\x08\x3f\x28\x04\xec\x4f\x7a\xb0\xc1\x09\xc1\xc2'
            b'\x16\x80\x3f\xd8\x08\x4b\x05\x42\x68\x15\xe5\x72\xe0\xa3\xc0'
            b'\x05\x2c\x60\x53\x3f\xe9\x65\x39\xbe\xeb\x62\x96\xb7\xbf\x92'
            b'\x94\xd7\x3a\xe1\x73\x0a\xe1\x30\xbb\x06\x1f\x65\x4b\xdf\x2f'
            b'\x29\x86\xc3\x71\x37\x79\x26\xe4\x81\x5f\x02\x5f\x53\xd8\x04'
            b'\x0c\x2f\x74\x6b\x60\xc1\x0a\xc0\x5a\xbb\x9d\x97\x14\xb8\x18'
            b'\xe1\x4f\x80\xcb\xb1\x27\xee\x16\x2c\x49\xaf\x95\x35\x4b\x2e'
            b'\xa7\xa7\xed\x0c\x6c\xfc\x92\x8d\x65\xae\xdc\x24\x3a\xf6\xa7'
            b'\x00\x11\x7b\x86\x9e\xe4\x99\x7d\xb7\x37\x9b\x08\x80\x3d\xa9'
            b'\x78\x2b\xf0\x65\x55\x1e\x44\x28\x2e\x54\x21\x58\x70\x02\x50'
            b'\x8e\xd1\x17\x84\x53\x80\x8f\x60\x1d\x7c\x4b\xe3\x6e\x57\xdc'
            b'\x18\xf1\x58\xbd\xe8\x8d\x1c\xd7\x75\x21\xe3\x6f\x8b\x62\x38'
            b'\x42\xae\xd4\x07\x40\xda\xef\x24\xe5\x8f\xb7\x0a\x94\xad\x7d'
            b'\xbf\xe6\x85\x03\x77\x11\x69\x18\xf7\x25\xcc\x86\x5d\xc0\x77'
            b'\x80\x7f\x04\x9e\x07\x74\xa1\x2d\x0b\x16\x8c\x00\xac\xfb\x21'
            b'\x95\x15\x7d\x27\x11\xd7\x02\x7f\x82\x8d\xd7\x5f\x30\x7d\x30'
            b'\x19\x0a\x74\x67\x8e\xe3\xac\xe5\xbf\x43\xd2\x6b\x05\x94\x48'
            b'\x43\xf6\x0c\x3d\xc1\xb6\x81\x07\xc8\x95\x7a\x41\x21\x9d\xe8'
            b'\x60\x65\xc7\x79\xac\x68\x7f\x55\xd9\x31\x28\x94\xc2\x11\x1e'
            b'\xdd\xf5\xaf\xf4\xe6\xb6\x34\x6b\x47\x46\xd8\x9c\x05\x5f\x01'
            b'\xbe\xe3\x29\xfd\xa3\x3e\xfc\xdd\x02\x49\x5e\xb2\x20\x82\x58'
            b'\xd6\xdd\x0a\x2a\x78\x22\x5c\x80\x72\x23\xf0\x31\x60\x05\x6e'
            b'\xf0\x03\x60\x10\x56\x75\x5d\xc0\xa2\x96\x93\xa8\x18\xfa\xbb'
            b'\x87\x1e\xe7\x99\x7d\x9b\x18\x2d\xf6\x11\x69\x40\xa4\x01\x85'
            b'\x70\x98\xbe\xdc\x16\x92\x5e\x96\xf6\xf4\x0a\x00\x7c\x93\x24'
            b'\x88\xf2\xf4\x8e\x6e\x8e\xfb\x32\x66\x8b\x00\x4b\xb0\x67\x38'
            b'\xce\x54\xe1\x65\xcf\xb0\xf3\xa2\x6b\xd1\x5f\x7e\x3b\xee\xa6'
            b'\xd5\x9e\x79\x1d\xb3\x7e\xdd\x46\xf0\x15\x42\x58\x2a\x86\x0f'
            b'\x62\x67\xfd\x55\x71\xb7\xab\xd1\xf0\xbd\x34\xed\xa9\x63\xca'
            b'\xff\x13\x8a\xe1\x30\xdb\x06\x1e\xa0\x14\xe6\x91\x71\x12\x29'
            b'\x40\x10\x15\xd9\x3e\xf0\x30\x4b\xb2\xa7\x8e\xed\x0e\xb4\xa7'
            b'\x56\xe0\x9b\x34\xa5\x28\x17\xf7\xa5\xcc\x85\x34\xf0\x76\xe0'
            b'\x1c\x09\xf9\x47\x84\xaf\x5f\x7f\x07\xbb\xa3\x70\x7e\xef\x16'
            b'\xcc\xdb\x93\x6a\x6b\x37\x02\xe0\x47\xc2\x9b\x45\xf8\x67\xe0'
            b'\xaf\x70\x83\x7f\x42\x8c\xf8\x63\x6b\x7b\x01\x72\xa5\x3e\x72'
            b'\xa5\xde\x43\x06\x7f\x05\x01\xf2\x41\x3f\xf9\xa0\x7f\xcc\x7c'
            b'\x4a\xf9\x6d\x18\x33\x6f\xe6\x92\x63\x81\xcf\xa2\x7c\x3b\x8a'
            b'\x78\x73\x24\x24\xd6\x6e\x8a\xbb\x49\xb5\x63\xde\x7c\x6b\x15'
            b'\x3e\x79\x0b\x04\x3e\x88\xd2\xad\xc2\x1f\x03\xff\x15\x9b\x2d'
            b'\xd7\x51\x35\x84\x79\xbe\x7a\x4a\x00\x97\xa1\xbc\xc2\xc0\x57'
            b'\x10\xbe\x7a\xfd\x46\xf6\x97\x3c\xf8\x1f\xf3\xcc\x37\x30\xaf'
            b'\x2c\x80\xeb\x36\xc1\x50\x0b\x02\x9c\xa3\xc2\x37\x80\xff\x86'
            b'\x1b\xfc\x47\x25\xd2\x80\x42\x60\xb7\xf2\x14\xc8\x24\xba\xc8'
            b'\x24\xba\x51\x3d\xf2\xb9\x0a\xb4\x24\xba\xc9\x24\x3a\xa9\xfc'
            b'\xba\x10\x0c\x11\x45\x4d\x13\x14\x34\x13\x96\x02\x9f\x41\xf9'
            b'\x5f\x11\x9c\x1f\x94\x90\xeb\x6e\x8b\xbb\x49\xd5\x65\xde\x08'
            b'\xc0\xba\x8d\x60\x20\x9b\x29\xf2\x41\xe0\xbb\xd8\xf5\x5c\xa3'
            b'\x67\xd0\x6d\x08\x82\x30\xcf\x60\x61\x47\xf9\x7f\x4a\xd2\xcb'
            b'\xb2\xaa\xe3\x7c\x12\x5e\x9a\xf1\x1a\xa0\x0a\x09\x93\xe6\xd8'
            b'\x8e\xf3\x49\x7a\x59\x2a\x0e\xc3\xc1\xc2\x4e\x82\x28\x1f\xf7'
            b'\x65\xd4\x8a\x04\xf6\xd8\xf7\x77\x52\x86\x3f\x34\x90\x5d\xb7'
            b'\x31\xee\x26\x55\x8f\xa6\xb7\xe3\xae\xbf\x1d\x82\x00\x8c\xe1'
            b'\x58\xe0\x53\xc0\x7b\xb1\x85\x30\x1c\xd3\x64\xaa\x6d\xc0\x97'
            b'\x07\x1e\x60\xb4\xd4\x0b\x40\x26\xd1\xcd\xaa\x8e\xf3\xe9\x69'
            b'\x7b\x05\x22\x1e\xf3\x64\x1b\x70\x26\x8c\x00\xdf\x12\xe1\x0b'
            b'\x0a\xdb\x8c\xc2\x0d\x4d\xee\x20\x6c\xea\xef\xec\xba\xdb\x20'
            b'\x1f\x42\xc6\xe7\x35\x02\xff\x1d\x9b\x83\x6f\xde\x58\x35\xf5'
            b'\xc4\x06\x02\x5d\xc6\x71\x5d\x17\x31\x59\x20\x50\x26\xd1\x55'
            b'\x9e\xf9\x2b\x28\x5b\xfb\x7e\xc5\x0b\x07\x7e\xd2\xac\x81\x40'
            b'\xb3\x41\x81\x7b\x04\x3e\x2d\x3e\xbf\xd6\xb0\xb9\xb3\x11\x35'
            b'\x6d\x1c\xc0\xba\x4d\x20\x42\x32\x61\xf8\x2f\x02\x7f\x87\x3d'
            b'\xae\xdb\xd4\x82\x16\x27\x8a\x32\x54\xd8\x4b\xda\xef\xa0\x35'
            b'\xb5\x84\x8a\x8e\x7a\x26\x45\xc6\xef\x20\xed\x77\xe0\x99\xca'
            b'\x8a\x4a\x00\x65\xf7\xd0\x93\x6c\x3e\x70\x37\x41\x54\x88\xbb'
            b'\xf9\xf5\x44\x80\x13\x80\xd7\x6b\xc4\x7e\x85\x67\x2f\xba\x96'
            b'\xb0\x59\x63\x06\x9a\x52\x00\xca\x6b\xb0\x2e\xe0\x3a\xe0\x73'
            b'\xd8\x32\x59\x8e\x39\x12\x6a\x91\xfe\xdc\x56\x04\x21\x9b\x5c'
            b'\x84\x6f\x92\x87\x28\xaa\xf5\xfd\x5b\xb3\x7f\xfb\xc0\x43\x6c'
            b'\x3e\x70\x77\x33\x9e\x03\xa8\x16\xdd\xc0\x65\x62\xe3\x4b\x1f'
            b'\xbd\xe8\x5a\xf2\xcd\x28\x02\x4d\x35\x63\x5e\xf7\x63\xf0\x8a'
            b'\xa0\x86\x55\x58\x93\xff\x77\x70\x8e\xbe\xaa\x63\x8f\x03\xaf'
            b'\x64\x69\xeb\xa9\x87\x1d\x07\x1e\x62\xb0\xb0\x93\xbd\xc3\xcf'
            b'\x30\x90\xdf\x4e\xd4\x3c\xc7\x81\x6b\x49\x11\xf8\x57\xe0\x33'
            b'\x1e\x6c\x2d\x00\x7f\xdb\x44\x7e\x81\xa6\x11\x80\xf5\xb7\x41'
            b'\x29\x09\x7e\x89\x33\x81\x0d\xd8\x9c\x7c\x4d\xd3\xfe\x66\x63'
            b'\x2c\x21\x88\x49\x8d\x05\xf9\x44\x51\x40\x10\x35\x55\x42\x90'
            b'\x7a\xa1\xc0\x5d\xc0\xba\xde\x0e\x1e\x5d\xd4\x0f\xcd\x92\x86'
            b'\xac\x29\xbe\xc7\xb5\x1b\x6d\x3e\xe8\x84\x4d\xbb\xbd\x01\xbb'
            b'\xde\x77\x38\x1a\x8d\x47\x80\xeb\x4c\x1b\xf7\x44\x23\xe8\x86'
            b'\x26\x48\x4a\xda\xf0\x02\xb0\x7e\x23\x18\xc1\x0b\x95\xff\x04'
            b'\x7c\x11\x5b\x3c\xd3\xe1\x68\x54\x5e\x54\xf8\x73\x02\xbe\x2f'
            b'\x86\xb0\xd1\x4b\x9a\x35\xb4\x00\xac\xdd\x08\x08\x09\x51\x3e'
            b'\x00\xfc\x35\x2e\xaa\xcf\xd1\x1c\xec\x01\x3e\x23\xca\x37\x15'
            b'\x4a\x8d\x5c\xab\xa0\x61\x77\x01\xd6\x6d\x02\x84\xb4\x28\x1f'
            b'\x05\xfe\x06\x5b\x66\xcb\xe1\x68\x06\x5a\x81\x4b\x10\x86\xd4'
            b'\xf0\xdb\x8b\x1b\x78\x9b\xb0\x21\x05\x60\xfd\x26\x10\x68\x41'
            b'\xf9\x04\xf0\x17\x40\x47\xdc\x6d\x72\x38\x66\x48\x06\xb8\x48'
            b'\xa0\xa0\xc2\x6f\x2f\xba\x96\xa0\x11\x45\xa0\xe1\x04\x60\xfd'
            b'\x6d\x80\x92\x55\x58\x0b\x5c\xcf\x02\xcf\xd3\xe7\x68\x6a\xd2'
            b'\xc0\x85\x02\x20\x3c\x7c\xd1\x7b\x29\x35\x9a\x08\x34\x94\x00'
            b'\x94\x03\x7c\xb2\x08\xeb\x81\xf5\x40\x76\x4e\x6f\xe8\x70\xc4'
            b'\x4f\x0a\x78\x8d\x80\x18\xe1\x81\x8b\xaf\xa5\x74\x5f\x03\x89'
            b'\x40\xc3\x08\xc0\xba\x8d\x65\xb3\xdf\x0e\xfe\x75\x40\x4b\xdc'
            b'\x6d\x72\x38\xaa\x44\x02\x38\x0f\x08\x55\x79\xf0\xa2\x6b\x09'
            b'\x7e\xf9\x9d\xb8\x9b\x64\x69\x08\x01\x28\x67\xea\x4d\x23\x7c'
            b'\x02\x6b\xf6\xbb\x99\xdf\x31\xdf\x48\x02\xaf\x16\x61\x14\xe1'
            b'\xe1\x46\x71\x0c\xc6\xbe\x0d\xb8\xd6\x0e\xfe\x84\x08\x1f\xc7'
            b'\xa6\xed\x6a\xdc\x35\x7f\xec\xbd\xe5\xa8\x1a\x3a\xf7\xb7\x98'
            b'\x25\xfd\xc0\x5f\x84\xca\xff\x34\x42\x29\xee\x7a\x04\xb1\xde'
            b'\xd2\xeb\x36\x81\x11\x4c\x14\xf1\x21\xe0\x06\xec\x01\x9f\xc6'
            b'\x42\x40\x05\x24\x04\xaf\x20\x48\x20\x48\x14\x77\xa3\x1c\xb3'
            b'\x45\x05\xd4\x57\xa2\x94\x12\xd9\xd4\x71\x71\x88\x41\x2f\xd6'
            b'\xd2\xfd\x06\x10\xc5\x99\x74\x34\x36\x01\x58\xbb\x09\x86\x7c'
            b'\x68\x2f\xf1\x2e\xe0\xcb\x40\x4f\x7c\xdd\x30\x09\x02\xde\x88'
            b'\x21\xbb\xd5\xa7\x65\x4b\x82\xf4\x5e\x0f\x7f\xd0\x60\x4a\x12'
            b'\xe7\x0c\xe2\x98\x03\x9a\x50\x82\xac\x52\x58\x14\x92\x3b\xb6'
            b'\xc4\xc8\xf1\x01\xc5\xee\xf0\x60\x21\xa4\xfa\xb1\x07\xf8\xf8'
            b'\x92\x80\x7f\x3f\xe0\xc1\x0d\x31\x05\x0b\xc5\x22\x00\x7f\x76'
            b'\x3b\x64\x4a\x50\xf4\x78\xbd\xc0\xd7\x69\xb4\xf0\x5e\x01\x29'
            b'\x09\xed\xcf\x26\xe8\x7a\x20\x4d\x66\x87\x8f\x57\xb0\x5d\xa5'
            b'\x6e\x19\x30\x2f\x10\x85\xc8\x87\x52\x57\xc8\xc0\x19\x45\xfa'
            b'\xcf\x2e\x50\x5c\x14\xd6\x5b\x04\x36\x03\x7f\xe8\x2b\xf7\x14'
            b'\x0d\xdc\x1c\x43\x62\x91\xba\xdf\xce\xd7\xdd\x0e\x5e\x08\x2a'
            b'\x9c\x89\x35\x81\xce\xab\xff\x65\x4f\xdd\x23\xfe\xb0\x61\xf1'
            b'\xcf\x33\x74\x3d\x92\xc2\xcb\x09\x7a\x58\x8e\x21\x37\xf9\x37'
            b'\x37\x87\xdc\xf4\xe5\x52\x87\xb9\x15\x01\xfb\xde\x30\xca\xd0'
            b'\x29\xa5\x7a\x8f\x8a\x07\x81\x0f\x89\xf2\x78\x98\x80\x9b\xdf'
            b'\x52\xdf\xbe\xa8\x7b\x5a\x70\x13\x41\x24\xac\x12\xb8\x91\x06'
            b'\x1c\xfc\xde\x88\x61\xd9\x8f\x5b\xe8\x7c\x34\x05\x11\x63\x83'
            b'\x5f\x01\x0f\xc1\x47\x30\xe5\x3b\x44\x44\x98\x30\x79\xbe\xa3'
            b'\x61\x51\x55\x02\x22\x4a\x6a\x1d\x39\x95\xaf\x2f\xb3\xc3\x67'
            b'\xc5\x2d\xad\xec\x79\xf3\x28\xfd\xaf\x2c\xd4\x53\x04\x5e\x0d'
            b'\x6c\x50\xe1\x23\x26\x60\x6b\xbd\xfb\xa3\xae\x77\x6f\x79\xaf'
            b'\xbf\x5b\xe1\xff\xc3\x26\xef\x6c\xa8\xd1\x23\x21\x2c\xfd\x69'
            b'\x0b\x8b\xef\xcb\x8c\x4d\xf3\x0a\xf8\x08\x8b\x25\xcd\x32\xd2'
            b'\xb4\x49\x82\x44\x39\x5d\x56\x32\x91\x22\x95\x6a\x69\xac\x8b'
            b'\x70\x4c\x8a\x02\x81\x46\x0c\x47\x05\xf6\x04\xc3\xec\x28\x0d'
            b'\x32\x12\x15\x0f\x79\x42\xd0\x1a\xb1\xeb\x9a\x11\x06\x4f\x2f'
            b'\xd6\xd3\xd4\x53\xe0\x5b\xaa\xfc\xbf\x22\xf4\xd5\xd3\x29\x58'
            b'\xb7\x7b\x77\xbd\x3d\xdc\x93\xd0\x88\x4f\x63\xb3\xf7\x26\xea'
            b'\x77\x99\xd3\xeb\x89\xb6\x67\x92\x1c\xf3\xfd\x56\xbc\x9c\x58'
            b'\xef\x3f\x90\xc5\x67\xb5\xb4\xb1\x4c\x32\xf8\xe3\xba\x4b\x81'
            b'\x54\x32\x4d\x26\xed\x42\x16\x9a\x0f\x21\x42\x19\x08\x73\x3c'
            b'\x5b\xd8\xcf\xb6\x62\x3f\xd1\x38\xc5\xcf\xf7\x84\x6c\xff\x2f'
            b'\x43\x14\x96\xd6\xd5\x27\x50\x04\x3e\x8f\xf0\x79\x94\x52\xbd'
            b'\x44\xa0\x2e\x81\x40\xeb\x6f\x87\x1b\x2e\x87\x3b\x9f\xe7\x77'
            b'\xb1\x39\xfc\x1a\x6b\xd4\x08\x98\xbc\xb0\xec\xae\x16\x32\xbb'
            b'\x7c\x30\xe5\x02\x18\xf8\xbc\x42\x3a\xe9\x91\x0c\x32\x81\x56'
            b'\x7a\x9e\x8f\xef\xbb\x8c\x64\xcd\x88\x00\x19\x93\x64\x99\xdf'
            b'\x0a\x02\xbd\xc1\xa8\x1d\xeb\x65\x1f\x90\x7a\x30\x72\x62\x5d'
            b'\xfd\x01\x1e\x70\x16\xb0\xa5\x77\x37\x4f\xbc\xf1\xc3\x50\x8f'
            b'\x68\xc1\x9a\x0b\xc0\xf5\x1b\x21\x52\xb8\xeb\x05\x2e\x00\xbe'
            b'\x44\xa3\x25\xf0\x14\x5b\xf0\x22\xbb\x25\xc1\xe2\x5f\x65\x90'
            b'\xc0\xce\xfe\x1e\xc2\x29\xd2\x4e\x8f\x64\x26\x7d\xa9\xe7\xf9'
            b'\x24\x9c\x00\x34\x35\x9e\x08\xdd\x5e\x0b\x79\x0d\xe9\x0b\x0f'
            b'\x16\x37\x4d\x0c\x19\x46\x4e\x0a\x08\xda\xea\x1a\xf4\x91\x01'
            b'\xce\xcc\xb4\xf2\x20\xc2\x8e\xd7\x5e\x0b\xb5\x3e\x37\x50\xf3'
            b'\x1c\xfa\x11\x20\xb6\x28\xe7\xdf\x00\xa7\xd4\xfa\xf3\x66\xd4'
            b'\xb6\x92\x90\xef\xf5\x18\xd9\xe1\x93\x78\x3c\x85\x3f\xce\xf4'
            b'\xef\x22\x39\xe5\xe0\x77\xcc\x0f\x14\x48\x88\xe1\xd4\xf4\x12'
            b'\x3a\x2b\x95\x90\x04\x12\x83\x86\xd6\x17\x63\x59\xa5\x9e\x02'
            b'\x7c\x5e\x60\x55\x3d\xa4\xa7\xa6\x02\xb0\x76\x13\xa8\xd0\x02'
            b'\x7c\x12\xb8\xac\x0e\xd7\x33\x2d\x34\x82\x7c\x9f\xc7\xe0\xb6'
            b'\x04\x23\xbb\x7d\x82\xfd\x3e\xe9\xbd\x07\x37\x44\x0c\xb0\x54'
            b'\xd2\x24\x5d\x8d\x91\x05\x81\x02\xad\x26\xc9\xca\x44\xc7\x98'
            b'\xc5\x2f\x11\xa4\xb7\xfb\x48\x29\x16\x17\xef\xa5\xc0\x9f\x0b'
            b'\xb4\xac\xaf\x71\x19\xb2\x9a\xdd\xe1\xeb\x36\x41\xa2\x05\x44'
            b'\xf9\x3d\xe0\x7d\x34\x88\xc7\x3f\x0a\x85\xd1\x3d\x3e\xa3\xbb'
            b'\x7d\xc2\x82\x9d\xee\x4d\x04\xe9\xd1\x83\xcd\xf3\x31\x74\x48'
            b'\x1d\x4c\x7b\xd5\x99\x3f\x6a\xfd\xfe\xcd\xfc\x98\x03\x82\xb0'
            b'\xc4\xcf\x92\x10\xbb\x2a\x56\x81\x54\x9f\xc1\x14\x89\xe3\xce'
            b'\x15\xe0\xf7\x15\xde\xd3\x3e\x02\xd7\xd7\xb0\x20\x69\x4d\xe2'
            b'\x00\xfe\xf4\x07\xf6\x0a\x82\x11\xce\xa3\x81\x4e\xf7\x69\x04'
            b'\xb9\xbd\x1e\xf9\xbe\x71\xae\x0f\xb1\x6a\xef\x95\x84\x4a\x58'
            b'\xb8\x41\x48\xd5\x7a\xf6\x17\x81\x74\x1a\xcc\x0c\x3f\x27\x08'
            b'\xa1\x38\x8d\x4a\x3c\xb3\x7d\xff\x66\x45\x15\xc2\x08\xc2\xc0'
            b'\x16\x8b\xac\xf4\xc1\xf4\xdf\x80\x16\x93\xc4\x17\x43\x51\x43'
            b'\x04\xf0\x72\x82\x84\xb6\x0a\x52\x0c\x64\x81\xf5\x03\x59\x7e'
            b'\xab\xca\x43\x9f\xbc\x0b\xbe\xf0\xa6\xea\x7f\x48\x4d\x04\x20'
            b'\x99\x04\x55\x16\x03\x9f\x01\x4e\xae\x69\x37\xcd\x80\xc2\x80'
            b'\x47\xa1\xff\x48\xbf\xa7\x50\x3e\x14\x32\xfe\xff\xb5\x94\x7d'
            b'\xe3\x61\xd6\xac\x41\x4e\x5a\x8d\xa4\x52\xd3\x7f\x9d\x2a\x3a'
            b'\x3a\x4a\xf4\xd4\x93\xe8\xb6\x29\x62\x46\x44\x30\x27\x9e\x84'
            b'\x9c\x76\xfa\xcc\xde\xbf\x59\xd1\x08\x0d\x42\x28\x14\x60\x64'
            b'\x18\xed\xeb\x43\xf7\xec\x41\xfb\x7a\xad\x18\x4c\x53\x08\xcc'
            b'\xe1\xdf\x79\x28\x87\xdc\x17\x31\x70\x32\xf0\x17\xc6\xf0\xa1'
            b'\xa0\xc4\xfe\x5a\x7c\x40\xd5\x05\x60\xed\x26\x50\xf0\x44\xf9'
            b'\x63\xa0\x61\xf2\xa1\x56\x1c\x7e\x93\x5a\x8a\xf5\xfa\xa2\x55'
            b'\x91\x8e\x0e\xcc\x19\xaf\x80\x6c\x76\xc6\xa6\xab\xb4\xb5\x61'
            b'\x3c\x43\xb8\x67\x37\xe4\xf3\x47\xde\xdc\xaa\x90\x4e\xdb\xc1'
            b'\xbf\x68\xd1\x9c\x4d\xe3\x66\xe1\x60\x2f\x2c\x43\x54\x21\x9f'
            b'\x47\x77\xee\x20\x7a\xe6\x69\xf4\xc0\x81\x19\xbe\x47\x43\x71'
            b'\x85\x2a\x1f\x51\xe5\x8b\x6b\x6f\x23\xbc\xa9\xca\x23\xaa\xaa'
            b'\xf6\xe1\x75\xb7\xdb\x99\x54\x94\xcb\x80\x8f\x11\x43\xa8\xf1'
            b'\x64\x14\x87\x0d\x61\xb1\x41\xbf\x62\x47\x75\x18\xef\x0b\xc8'
            b'\x64\x90\x93\x56\x63\x2e\x79\x1d\x72\xec\xb1\x71\xb7\x6c\x2e'
            b'\x24\x80\x8f\x8b\x70\x99\x11\xb8\xee\xd6\xea\xbe\x79\x55\x07'
            b'\xa8\x44\xa0\xd0\x23\x76\xdd\xdf\x38\xc7\x7b\x15\x82\x51\x19'
            b'\xdb\x93\x8c\x15\x11\x74\xa0\x9f\xe8\xc9\x27\x90\xd5\xab\x91'
            b'\xe4\xcc\x4c\x74\x1d\x1d\x21\x7a\xf2\x49\x6b\xee\x4e\x64\xda'
            b'\x8a\x40\xa1\x80\x3e\xfd\x14\x2c\x94\x25\x00\x58\x5f\x87\x31'
            b'\x90\x48\xd8\xbf\xcb\x42\x20\x1d\x1d\x98\x73\x5f\x4d\x94\xcf'
            b'\xa3\x7b\xf7\x36\xeb\xd9\x8d\x1e\xe0\x93\x28\x4f\x18\xc3\xae'
            b'\x6a\xbe\x71\xd5\x04\x60\xfd\x6d\x20\x21\x26\xf2\xf8\x20\xb6'
            b'\x84\x57\xc3\xa0\x91\x10\x16\x4c\xfc\x83\xbf\x42\x14\x11\x3d'
            b'\xf3\x34\xbc\xf4\xe2\xcc\x9d\x74\x61\x79\xad\x3b\xe5\x05\x2b'
            b'\xd1\x8b\x9b\x61\xc7\xf6\x85\xe1\x04\x34\x06\xf1\x7d\x48\xa5'
            b'\x90\x8e\x0e\x64\xc5\x31\xc8\xf2\x15\xe0\xfb\x76\xc9\xd5\xde'
            b'\x8e\x39\xed\x0c\xc2\xbe\xbe\x83\x0e\xc2\xe6\xe3\x75\x2a\x7c'
            b'\x44\xe0\xaf\xd7\x6f\x24\xbc\xb1\x4a\xa1\xc2\x55\x11\x80\x3f'
            b'\xbd\x03\x08\x41\x3d\x2e\x00\x3e\x52\xad\xf7\xad\x16\xaa\x10'
            b'\x85\x71\xb7\x62\x82\x46\xe5\x72\x33\x7f\xdd\x74\x67\xb0\xd9'
            b'\xbe\x7f\x93\x52\xf1\x74\xe8\xee\xdd\xf0\xe2\x8b\x98\x93\x4f'
            b'\xc6\xbc\xf2\x6c\x6b\x11\x28\xc8\xf2\xe5\xc8\xa2\xc5\xe8\xee'
            b'\x5d\xcd\x6a\x05\x78\xc0\x1f\x29\xfc\x54\x85\x9f\x7f\xea\x87'
            b'\xf0\xf9\xb7\xcf\xfd\x4d\xab\x32\x50\x93\x76\x70\x75\xa9\xcd'
            b'\xe6\xbb\x2a\xc6\x4e\x9a\x98\x46\xf5\x83\xd5\xfa\x46\x6c\xce'
            b'\x1b\x7d\xee\x94\x4a\x44\xcf\x3d\x07\x5d\x8b\x30\xab\x57\x5b'
            b'\x31\x4c\xa5\x90\x65\xcb\xac\x00\x34\x2f\x2b\x80\xeb\x04\x1e'
            b'\x2f\x25\xe8\xab\xc6\x1b\xce\xd9\x3e\x5c\xb7\xd1\x2e\xad\x15'
            b'\xde\x03\xc4\x90\xd3\xc4\xe1\x38\x0c\x11\x08\x4a\xe8\xae\x9d'
            b'\x87\x98\xfc\xd2\xd1\x61\x97\x05\xcd\xcd\x5b\x51\x7e\xef\xcc'
            b'\x56\xb8\xae\x0a\x51\x82\x55\x59\x20\x1a\x38\x0d\xf8\x28\xb6'
            b'\x08\x82\xc3\xd1\x00\x08\x0c\x0e\x1e\x1a\x07\x90\xcd\x82\xd7'
            b'\xf4\x02\x90\x02\x3e\xfa\xf8\x30\xa7\x56\x63\xf0\xce\xe9\x3d'
            b'\xd6\xdf\x06\x12\x91\xc0\xae\xfb\x4f\x8f\xbb\x67\x1c\x8e\xf1'
            b'\x68\xb1\x00\xd1\xb8\x23\x35\xc9\x14\x78\x66\x3e\xc4\x46\x9c'
            b'\x01\x7c\x38\x82\xc4\xda\x39\x5a\x01\xb3\x16\x80\x4f\xff\xc4'
            b'\x9a\xfe\x91\xe1\xb5\xc0\xef\xc5\xdd\x23\x0e\xc7\x11\x44\xd1'
            b'\x21\x83\x5d\x3c\x6f\x3e\xf9\x45\xde\x63\xe0\x62\x01\x3e\xf3'
            b'\xa3\xd9\xbf\xc9\xac\x05\xa0\x68\xd3\xa6\xb5\x89\x35\xfd\x97'
            b'\xc6\xdd\x1b\x0e\xc7\x11\x1c\x3e\xd3\xcf\xaf\x2d\xd1\x65\xc0'
            b'\xc7\x04\x5a\x8b\x73\xc8\xea\x31\xab\x1e\xf9\xf3\x3b\xca\x96'
            b'\x95\x70\x05\xf0\xd6\xb8\x7b\xc2\xe1\x58\xa0\x5c\xae\x70\x85'
            b'\x00\x7f\x36\xcb\xa5\xc0\xac\x04\x20\x8a\xc0\xf3\x58\x0c\xfc'
            b'\x31\xd0\x1a\x77\x2f\x38\x1c\x0b\x94\x56\xe0\x23\x21\x2c\x9e'
            b'\xad\x6b\x73\xc6\x02\xb0\xee\x56\x9b\x2a\x5b\x95\xb7\x03\x17'
            b'\xc5\xdd\x03\x0e\xc7\x02\xe7\x12\x81\xb7\xa9\x07\xeb\x66\xe1'
            b'\x0b\x98\xb9\x05\x60\x80\x80\x15\xc0\x1f\xe2\xb6\xfd\x1c\x8e'
            b'\xb8\x49\x01\x1f\x92\x80\x9e\xd9\x64\xf8\x9c\x91\x00\xac\xbf'
            b'\x03\x22\x9b\x21\xe5\xed\xc0\xb9\x71\x5f\xb9\xc3\xe1\x00\xe0'
            b'\x3c\x84\xb7\x87\x06\xae\x9f\xe1\x69\xc1\x19\x09\x80\x86\x60'
            b'\x52\x2c\x07\x7e\x9f\x46\xcb\xeb\xef\x70\x2c\x5c\x92\xc0\xfb'
            b'\xbd\x88\xe5\xd1\x0c\x6d\xfa\x69\x3f\xfd\x13\x9b\xc0\xb3\x39'
            b'\xb3\xde\x06\x9c\x13\xf7\x15\x3b\x1c\x8e\x43\x38\x17\xb8\x3a'
            b'\x8c\xe0\x93\x77\x4c\xff\x45\xd3\x16\x00\x4f\x21\x34\x2c\x01'
            b'\xae\xc5\x2a\x8e\xc3\xe1\x68\x1c\x92\xc0\x7b\x3c\xc3\xa2\x60'
            b'\x06\x27\x5f\xa7\x25\x00\x9f\xb8\xb5\x1c\x40\xa5\xbc\x05\x5b'
            b'\xcc\xd0\xe1\x70\x34\x1e\xe7\x03\x97\x2a\xf0\xc9\xdb\xa7\xf7'
            b'\x82\x69\x09\x40\x39\x7c\xba\x1d\x3b\xfb\xa7\xe3\xbe\x4a\x87'
            b'\xc3\x31\x21\x2d\xc0\xef\x19\xc8\x06\xd3\xac\x2a\x72\x54\x01'
            b'\xf8\xd9\xc1\x68\xca\x0b\x71\xfb\xfe\x0e\x47\xa3\x73\xa9\xc2'
            b'\x05\xd3\x7d\xf2\x51\x05\xe0\x56\x5b\xd5\x37\x09\xfc\x2e\xd0'
            b'\x11\xf7\xd5\x39\x1c\x8e\x29\xe9\x02\xde\x0d\x24\xd7\x4d\x23'
            b'\x3c\x78\x5a\x4b\x00\x55\x4e\x07\xde\x1c\xf7\x95\x39\x1c\x8e'
            b'\x69\x71\x39\xd3\x3c\x9e\x3f\xa5\x00\xac\xdd\x04\x09\x5b\x21'
            b'\xf9\x1a\x1a\xad\xaa\xaf\xc3\xe1\x98\x8c\x63\x80\xab\x4d\x97'
            b'\x0d\xdd\x9f\x8a\x29\x05\x40\x14\x82\x24\x3d\x58\x01\x70\x38'
            b'\x1c\xcd\x81\x00\xd7\x44\x7d\xf4\x1c\xcd\xc6\x9f\xf4\xd7\x7f'
            b'\xfe\x63\xfb\xb7\x2a\xaf\x03\x5e\x11\xf7\x15\x39\x1c\x8e\x19'
            b'\xf1\x0a\xe0\x12\x80\xcf\xfe\x64\xf2\x27\x4d\x2a\x00\x61\x00'
            b'\x28\x29\xec\xec\x9f\x89\xfb\x6a\x1c\x0e\xc7\x8c\x68\x01\xae'
            b'\x31\x42\x2a\x3f\x45\x19\x89\xa9\x0d\x04\xe1\x64\xe0\x75\x71'
            b'\x5f\x89\xc3\xe1\x98\x15\xaf\x8f\x94\xd5\x53\x65\x40\x9c\x50'
            b'\x00\xd6\xdf\x66\xeb\xa3\x03\x6f\xc4\x39\xff\x1c\x8e\x66\x65'
            b'\x25\x70\x59\x14\xc2\x27\x7f\x3c\xf1\x13\x26\x14\x00\x15\x10'
            b'\xa5\x0d\x9b\xee\xab\xf9\x13\xa9\xcd\x9b\x3c\x90\x0e\xc7\x8c'
            b'\xf0\x80\xb7\x1a\x9f\xd6\xc9\x2a\xa2\x4d\x35\xb8\x4f\x07\xce'
            b'\x8b\xfb\x0a\x1c\x0e\xc7\x9c\x78\xb5\x28\xa7\x4d\xf6\xcb\x23'
            b'\x04\x60\xfd\xc6\xb1\x4a\x5a\x97\x02\x4b\xe2\x6e\xbd\xc3\xe1'
            b'\x98\x13\x4b\x14\x2e\x15\x85\x75\x9b\x8e\xfc\xe5\x11\x02\xa0'
            b'\x80\x40\x3b\xf0\x86\xb8\x5b\xee\x70\x38\xe6\x8c\x00\x6f\x50'
            b'\xa1\x6d\xa2\x1a\x99\x66\x92\x57\x9c\x02\x9c\x1d\x77\xcb\x1d'
            b'\x0e\x47\x55\x38\x07\x38\x79\xa2\x5f\x1c\x22\x00\xd7\x6d\xb2'
            b'\x72\xa1\x70\x31\xb0\x38\xee\x56\x3b\x1c\x8e\xaa\xb0\x44\xe1'
            b'\x12\x51\xf8\xb3\xc3\xf2\x04\x1c\x22\x00\x46\x41\x6d\x00\xc1'
            b'\x25\xcc\x07\xef\xbf\xc3\xe1\x00\x30\x02\x17\xab\x21\xe3\x1f'
            b'\x96\x27\x60\xa2\x7a\x02\x2b\x70\x19\x7f\x1b\x83\x5a\x17\xb1'
            b'\x3c\x5a\x9d\xbc\xb8\x3f\xdf\x51\x4d\xce\xc3\x8e\xed\xcd\xe3'
            b'\x7f\x38\x91\x00\x9c\x0b\x2c\x8f\xbb\xb5\x0b\x1e\x63\x90\xf6'
            b'\x76\xf0\x6b\x94\x7c\xb9\x54\x42\x87\x06\x0f\xad\x9e\x5b\x41'
            b'\x15\x92\x49\xa4\xad\x0d\xcc\x1c\x0a\xcf\xcd\xf6\xf3\x1d\xb5'
            b'\x60\x39\xca\x39\x4c\x26\x00\xeb\x37\x81\xef\x23\xa5\x12\xe7'
            b'\xe3\xd2\x7e\xc5\x8b\x31\x78\x6f\x7a\x0b\xfe\xbb\xfe\x33\xb4'
            b'\xb5\x03\xd5\x9e\x89\x05\x06\x07\x09\xbe\xff\x6f\x84\x77\xdd'
            b'\x79\xe8\x20\x54\x45\xda\xdb\xf1\xae\x7d\x1f\xde\x05\x17\xda'
            b'\x92\xda\xf5\xfc\x7c\x47\xad\xc8\x00\xe7\x0f\xa5\xf8\xb7\xb5'
            b'\x9b\xe0\xa6\x2b\xec\x0f\xc7\x04\x20\x52\x28\x96\xe8\x14\x9b'
            b'\x58\xd0\x11\x17\xe5\x01\xe8\xbf\xf3\x5d\xc8\x09\x27\xd6\xee'
            b'\x73\x16\x2f\xc6\x7f\xc7\xbb\x88\xee\xbf\x1f\xed\xef\x3b\x68'
            b'\x8e\x47\x11\xe6\xec\x73\xf1\xaf\xba\x06\x52\x35\x2c\xfc\x34'
            b'\xd9\xe7\x3b\x6a\xc9\xf9\x6d\x05\xba\x80\xbe\xca\x0f\xc6\x1c'
            b'\x7d\x62\x1f\xc7\x31\xc9\x76\x81\xa3\xce\xd4\x78\xf9\x3d\x25'
            b'\x9e\xa9\xcb\x80\xd4\x28\x8a\xf9\x42\x17\x1c\x6b\x14\x8e\x1d'
            b'\xff\x83\xc3\x7d\x00\xaf\xc4\xe6\x14\x73\xc4\x85\x08\x3a\x38'
            b'\x48\xf0\x1f\xff\x8e\xff\xce\xff\x0c\xed\x1d\xd4\xc6\x04\x1f'
            b'\x20\xf8\xfe\xff\xb1\xeb\xf0\xf1\x83\xdd\x18\xa2\x47\x1e\x21'
            b'\xbc\xeb\x4e\xcc\x39\xe7\x82\xef\xd7\xe0\xf3\x41\x0f\x1c\x20'
            b'\xfc\xb7\xef\xa1\x83\x83\x6e\xf6\xaf\x1f\x5d\x02\xaf\x02\x1e'
            b'\xab\xfc\xc0\x07\x9b\xfa\xab\xe8\x21\xc9\x80\xb3\x71\x45\x3f'
            b'\xe2\x27\x8a\x08\xef\xba\x93\xe8\xfe\xfb\x21\x51\x67\x27\xa0'
            b'\x08\xda\xd7\x4b\xe9\xab\x5f\x46\xda\x5a\x41\x6a\xb4\x1b\x5c'
            b'\x2c\xd8\xc1\xef\xa8\x27\x49\xe0\xec\x54\x81\x6f\xad\xbf\x0d'
            b'\xbd\xf1\xaa\xb2\x00\x08\x90\x0c\xe9\xc0\x5a\x00\x8e\x46\x20'
            b'\x8a\xec\xda\xb8\x96\x4c\x36\xf3\x8a\x40\x21\x8f\x16\xf2\xf1'
            b'\x7c\xfe\x02\x42\xc4\x90\x30\x19\x82\xa8\x40\xa4\xc1\xdc\xdf'
            b'\xf0\xe8\x9c\x55\x48\xd1\x0e\x0c\x40\x65\x09\x60\x2d\xbc\x25'
            b'\xc0\xea\xb8\x3b\xc4\x31\x8e\x38\x07\x88\x1b\x9c\x35\x47\xc4'
            b'\xb0\xb2\xfd\x3c\x56\x76\x9c\xc7\xde\x91\xa7\x79\xa9\xf7\x17'
            b'\x44\x5a\xaa\xf5\xc7\x9e\x0c\x2c\xa5\x2c\x00\xe3\xed\xbb\xd3'
            b'\x70\xeb\x7f\x87\xa3\x2e\x28\xd0\x92\xe8\xe6\xb8\xae\x8b\x68'
            b'\x4f\x2f\x67\x55\xe7\x6b\xe8\xca\xac\xaa\x87\x4b\xb4\x0b\x38'
            b'\xb5\xf2\x1f\xf3\xe9\x3b\x41\xed\x32\xf0\x34\x20\x1b\x47\x47'
            b'\x54\x1e\x0e\xc7\x82\x41\x21\x9b\x5c\x4a\xca\xcf\x12\x69\x48'
            b'\xc2\x64\x68\x4f\x1f\x53\x8f\x4f\x6e\x05\x4e\x8f\x22\xf8\xd4'
            b'\x9d\x60\x8a\x01\x88\x4f\x02\x58\x13\x47\x3f\xb4\xa7\x96\xb3'
            b'\x7a\xd1\xa5\x2c\xca\x9c\x80\x4b\xdd\xe3\x58\x48\x64\x12\x9d'
            b'\x18\x29\x3b\x79\x45\xc8\xf8\x9d\x98\x5a\x39\x5d\x0f\xe5\x64'
            b'\x49\x90\x28\x05\xe0\x97\xa7\xdf\x36\x62\x10\x80\xa4\x97\x65'
            b'\xcd\x92\xb7\xb2\xa8\xe5\x24\x86\x5a\x77\xf3\xe8\xae\x7f\x65'
            b'\xb8\xb8\xcf\xc9\x40\x85\x5a\xc7\xe2\xcf\x14\xe7\x17\xa8\x1a'
            b'\x52\x1e\xf0\x22\x06\xd5\x08\x14\xd2\x89\x0e\x3c\x49\x10\x68'
            b'\x61\xee\x1f\x30\x35\x6b\x88\x68\x55\xe8\xf3\xcb\xb7\x58\xb7'
            b'\xc0\xaa\x7a\x76\x80\x02\xad\xa9\x65\xb4\xa5\x96\x13\x69\x44'
            b'\x36\xb9\x98\xee\xcc\xf1\x0c\x17\xf6\x39\x43\x00\x6a\x7f\x16'
            b'\x60\xa6\xb8\xd8\xfd\xaa\xe2\x99\x04\x99\x44\xd7\xb8\xb5\xaf'
            b'\x92\xf1\x3b\xf1\x4c\x92\x52\x54\xa8\xf5\x10\x38\x4e\xd4\x46'
            b'\x04\xfa\xe5\xf3\xff\xc7\x01\x6d\x75\xed\x01\xb5\x4e\x10\xcf'
            b'\x24\x00\x45\xc4\xa3\x25\xb9\xc8\x4d\x32\x50\x87\xb3\x00\x33'
            b'\xc5\xc5\xee\x57\x13\x55\x68\x4d\x2e\xa5\x2d\xd5\x83\x96\xbf'
            b'\x5b\x05\x52\x7e\x1b\x1d\xe9\x63\xc8\x0f\x3d\x63\x13\xf3\xd6'
            b'\xae\x09\xed\xd8\x31\xff\x62\x25\x0e\xe0\x04\xea\xec\x00\x14'
            b'\x81\xb4\xdf\x81\xc1\x47\xb1\x37\x54\xda\xb7\x26\x50\x58\xfb'
            b'\xad\x90\xc6\xa5\x5e\x67\x01\x66\x8a\x8b\xdd\x9f\x15\x5a\xfe'
            b'\x43\x44\xf0\x8c\x8f\x27\x49\xb2\xc9\xc5\x9c\xd8\xfd\x06\x52'
            b'\x7e\x1b\x07\xc5\x5d\xf1\x4c\x8a\xd5\x8b\xde\x88\x91\x04\xfd'
            b'\xb9\xad\x04\x51\x91\x50\x4b\x44\x1a\x02\x55\x15\x84\x16\xec'
            b'\x98\xbf\xdb\x2f\xa7\x00\x3a\x8e\x89\x8f\x06\xd7\x0c\x23\x3e'
            b'\x99\x44\xe7\x58\x0a\x22\x54\x49\xfb\x9d\x18\x93\x20\x0c\x17'
            b'\xb0\x00\x54\x88\x7b\xd2\x77\xcc\x19\x11\x43\x47\x6a\x05\x9d'
            b'\xe9\x55\xa4\x13\x1d\x64\x12\x1d\x64\xfc\x2e\x52\x7e\x3b\x09'
            b'\x6f\xa2\x62\x5b\x4a\x36\xb9\x94\xd3\x97\xbd\x8d\x62\x30\x44'
            b'\xae\x34\x40\x3e\x18\x20\x57\xea\x65\xb0\xb0\x8b\xbe\xdc\x56'
            b'\xc2\xa8\x58\x8d\xa6\x25\x80\xe3\x4d\x64\x9d\x80\x29\x0e\x3b'
            b'\x20\x50\x6b\x14\xeb\x00\x6c\x4d\x2e\x1d\x73\x74\x29\x90\x4e'
            b'\xb4\x91\xf6\xdb\x29\x06\xa3\x0b\x77\x82\xa9\xcb\x59\x80\x19'
            b'\x37\x6a\xf2\xb3\x03\x8e\x49\x59\xde\x76\x16\xab\x17\xbd\x91'
            b'\x94\xdf\x86\x88\x19\x33\x07\x0e\xde\xf1\x13\xa1\x78\x92\xa0'
            b'\x25\xb1\x88\x96\xc4\xe2\xf2\x04\xa9\x04\x51\x81\x97\x07\x1e'
            b'\x64\xf3\x81\xbb\xab\x15\x31\xb8\x32\x12\x92\x3e\x42\x0b\x5a'
            b'\xfb\xea\x3f\x15\x53\x08\x81\x84\x49\xb1\xb2\xe3\x5c\xb2\xc9'
            b'\x25\x63\xdd\x01\x4a\xd2\x6b\xe5\xb8\xce\x0b\x79\xe1\xc0\x4f'
            b'\xc9\x07\x83\xa8\xea\x98\xdd\xb3\xa0\x6e\xb9\x7a\x9c\x05\x98'
            b'\x29\xce\x09\x38\x23\x8c\xf8\x2c\xce\x9e\x4c\x26\xd1\x45\xa4'
            b'\xa1\xf5\xf4\xcf\x00\xad\x44\xc7\x28\x80\x90\xf0\x32\x74\x67'
            b'\x4e\x64\x8b\xb9\x8f\x28\xac\x8e\x00\x28\x64\x7d\x85\xac\xd8'
            b'\x7a\xe2\x35\x41\x30\x24\xfd\x2c\x69\xbf\x83\x96\x44\x37\x2d'
            b'\x89\x6e\xda\xd2\x2b\xe8\x6e\x39\x01\x11\x8f\xc3\x95\xb0\xa7'
            b'\xfd\x2c\xb2\xc9\x25\xf4\xe5\xb6\x92\x0f\xfa\xc9\x95\x06\xc8'
            b'\x05\x7d\x14\x4a\x83\x94\xa2\x5c\xad\x9a\xd9\x78\xd4\xe3\x2c'
            b'\xc0\x4c\x71\x33\xff\xb4\x89\x34\x60\xd7\xe0\xa3\x64\x13\x8b'
            b'\xc9\x24\xba\xf0\x4c\xa2\x7c\xbf\x03\xaa\xe3\x26\xbe\x23\x11'
            b'\x04\x25\x22\xd2\x08\x25\x42\x35\x62\xb4\x78\x80\x97\xfa\xee'
            b'\xa5\x14\x56\x6d\x0c\x1c\x23\x42\x8b\x2f\xca\x22\xa0\xa3\x16'
            b'\x9d\xe0\x9b\x14\xc7\x76\x9e\xcf\xf2\xb6\xb3\x48\x7a\xad\x78'
            b'\x26\x89\x27\x3e\x94\x2f\x70\x22\x33\x48\x10\x3a\xd2\xc7\xd0'
            b'\x91\x59\x89\x6a\x48\x18\x05\x84\x5a\x64\xa4\xb8\x9f\xad\x7d'
            b'\xf7\xb1\x6f\xe4\xb9\x5a\x34\xb5\x31\x71\x03\xae\xa9\xd9\x37'
            b'\xf2\x3c\x43\x85\x3d\xb4\xa6\x96\x91\x49\x74\x92\xf1\x3b\xc9'
            b'\x24\xba\x68\x4b\x2d\x23\x93\xe8\x9e\xf0\x35\x91\x06\xec\x1b'
            b'\x7e\x8e\xbe\xdc\x16\x82\x28\x4f\xa8\x25\x82\xa8\xc0\x48\x71'
            b'\x1f\x85\x60\x98\x2a\x2e\x07\x3b\x81\x6e\x1f\x9b\xff\xaf\xea'
            b'\xa9\x5f\x14\xe8\x6e\x39\x91\x13\xba\x5f\x87\x6f\x52\xd6\x9c'
            b'\x47\x0f\x9a\x36\x53\xbe\x56\xcb\xbe\x01\xc1\x33\x09\x3c\x92'
            b'\xa4\x5b\xda\xf1\x24\x41\x7f\x7e\x3b\xa5\x70\xb4\xda\xcd\x75'
            b'\x38\x6a\x80\x5a\x27\x5e\x30\x30\xb6\x13\x60\x9d\xdf\xed\x9c'
            b'\xd0\xf5\x3a\x7a\xda\xcf\x42\x0e\x59\xdc\x2a\x3b\x06\x1e\xe6'
            b'\x85\x03\x3f\xa5\x14\x8e\x0b\x06\xaa\xcd\x96\x60\x1a\x61\x85'
            b'\xc1\x0a\x40\x4d\x72\x00\x16\x83\x61\x8a\xc1\xb0\xbd\x06\x91'
            b'\xf2\xc5\x4e\xef\x52\xec\xb3\x0d\x22\x06\x11\x21\xd2\x80\xe1'
            b'\xe2\xde\x7a\x9c\x96\x72\xcc\x17\xa2\x08\x2d\x14\xac\x25\x25'
            b'\x62\xff\x1d\x83\x0f\x43\xa8\x18\x73\x4a\xa4\x25\x86\x0b\x07'
            b'\xd8\xdc\x7b\x0f\xa3\xc5\xfd\xe3\x04\x40\x28\x04\xc3\x6c\x1f'
            b'\xf8\x8d\x0d\x04\x12\x0e\x3e\x6a\xd3\xac\x14\xca\x72\x1f\x58'
            b'\x46\x0d\x92\x80\x08\xd0\x9f\xdf\xce\x13\x7b\xfe\x83\x25\xd9'
            b'\x35\x64\x93\x8b\x48\xfb\x9d\x24\xbd\x2c\xbe\x49\xe3\x9b\xe4'
            b'\x24\xeb\x20\x29\x77\xd2\x5e\x0a\xe1\x10\x61\x54\x24\x8c\x4a'
            b'\x0c\x17\xf7\xb2\x7b\xe8\x09\xc2\xc8\x09\x80\x63\x1a\x88\x40'
            b'\xa1\x80\x3e\xfd\x14\x9c\x76\x3a\x00\xfa\xf4\x93\x50\x11\x84'
            b'\xb8\x9b\x16\x0c\x33\x5c\xdc\x47\x6b\x6a\x99\x8d\xfd\x00\x0a'
            b'\xc1\x20\x85\x70\xa8\x5e\x0e\xef\x14\xb0\xcc\xc7\x56\x00\xaa'
            b'\x51\x0c\x80\xd2\x97\xdb\x46\x7f\xee\xe5\xb1\x20\x88\x84\x97'
            b'\x21\x9b\x58\xcc\xf2\xf6\x57\xb2\x24\xbb\xc6\x6e\x8f\x1c\xec'
            b'\x1a\x82\x30\xc7\xe6\xde\xbb\xed\x60\xd7\x12\x3a\xce\x11\xe2'
            b'\x70\xcc\x08\x55\xa2\x17\x37\xc3\x8e\xed\xf6\xff\x85\x42\xc3'
            b'\x9c\xaf\x88\xb4\x44\xbe\xd4\x7f\xf0\x07\x22\xe4\x83\x41\xa2'
            b'\xfa\x4d\x70\x3e\xb0\xb8\x22\x00\x35\xc3\xaa\x99\x12\x46\x25'
            b'\x42\x4a\x14\xc2\x11\x86\x0b\xfb\xe9\xcf\xbf\x8c\x2c\xf3\x58'
            b'\x9a\x5d\x33\x66\x09\x08\xb0\x7b\xf8\x09\x5e\x1e\x78\x88\x48'
            b'\xc3\x85\xb5\xf5\xe7\xa8\x0d\xaa\x90\x2b\x7b\xce\x1b\xc8\xa9'
            b'\xaa\x0a\xf9\x60\x00\xd5\x90\xca\x28\xc9\x07\x83\xf5\x8e\x82'
            b'\x5d\x64\xa8\x73\x12\x90\xca\x7a\xa8\x10\x8c\xb0\x7f\xe4\x79'
            b'\x22\x0e\xce\xec\xa1\x06\xf4\xe7\x5e\x26\x8a\xdc\xe0\x77\x54'
            b'\x91\xca\x62\xba\x91\x10\x18\x2d\xf5\x96\x97\xb4\x82\x6a\x44'
            b'\xbe\xd4\x5f\x6f\x03\xa5\xdb\x50\xa3\x2d\xc0\xe9\x74\x40\xbe'
            b'\xd4\x5f\x36\x79\xac\x73\x30\xd2\x12\x85\x60\x60\x81\x45\xfd'
            b'\x38\x16\x22\x02\x0c\x15\x76\x33\x52\xdc\x8f\x11\x43\x31\x1c'
            b'\x61\x20\xbf\xa3\xde\xf7\x7e\xbb\x8f\x3d\x19\x14\x0b\xb9\xa0'
            b'\x9f\x50\x8b\x78\xe5\x5d\xc8\x30\x2a\x91\x0f\x86\xe2\x6a\x8e'
            b'\xc3\x51\x57\x0a\xc1\x10\x2f\x1c\xf8\x09\xc7\xb4\x9f\x43\x6f'
            b'\xee\x45\x06\x0b\x3b\xea\x3d\xf7\xb5\xfb\xd8\x14\x41\x75\x47'
            b'\x80\x52\x38\x4a\x31\x18\x21\xe5\xd9\x93\xc8\xc5\x70\x84\x20'
            b'\xca\x3b\x03\xc0\xb1\x60\x38\x30\xfa\x22\x7d\xb9\xad\xe5\x13'
            b'\x7f\x75\x77\x50\xb6\x19\xec\xd1\xc0\x58\x08\xa2\x02\x43\xc5'
            b'\x3d\x63\x6b\xb4\x91\xe2\x3e\x82\xa8\xe6\xd9\x50\x1c\x8e\x06'
            b'\x42\xcb\x87\x7b\x62\xd9\x9d\xc8\xf8\xc4\x58\x08\x34\xd4\x80'
            b'\x1d\x03\xbf\xa1\x3d\xb5\x1c\xc1\xb0\x73\xf0\x51\x42\x0d\x9c'
            b'\x05\xe0\x70\xd4\x87\x78\x05\x40\x80\xbe\xdc\x56\x7e\xbb\xf3'
            b'\xbb\x20\x90\x2b\xf6\xba\xc1\xef\xa8\x3e\x15\xd7\x7a\xa3\xed'
            b'\x04\xc4\x4f\xda\xa7\xce\x89\x40\x8e\x44\x19\x29\x1d\x00\x9c'
            b'\xf3\xdf\x51\x03\x44\x20\x9d\xb6\x16\x76\xad\x2b\x1d\x35\x1f'
            b'\xbe\x0f\x78\x71\xb7\xc2\x0d\x7c\x47\x4d\x10\xc1\x9c\x78\x12'
            b'\x72\xfa\xe9\x10\x29\xd1\x13\x8f\xa1\x5b\xb7\xc6\xdd\xaa\x46'
            b'\xc2\x33\x34\x80\x00\x38\x1c\x55\x47\x15\x52\x29\xe4\xb4\xd3'
            b'\x91\xee\x45\xc8\xe2\xc5\x98\xd3\x5f\x01\xa9\x14\xf1\x67\x58'
            b'\x6a\x18\xbc\x98\xcd\x7f\x87\xa3\x86\x18\x83\xa4\x52\x63\x3e'
            b'\x00\x69\x69\x01\xcf\x1b\xcb\x4c\xe5\xb0\xb5\x01\xc3\xb8\x1b'
            b'\xe1\x70\x38\x62\x21\x74\x02\xe0\x70\x2c\x5c\x42\x03\xd4\xa5'
            b'\x28\xb9\xc3\xe1\x68\x38\x02\x03\xb8\xbd\x11\x87\x63\x61\x92'
            b'\x77\x02\xe0\x70\x2c\x5c\x72\x06\x70\x19\x36\x1d\x8e\x85\x49'
            b'\xce\x00\xee\xfc\xad\xc3\xb1\x30\x19\x32\xc0\x60\xdc\xad\x70'
            b'\x38\x1c\xb1\x30\xe8\x04\xc0\xe1\x58\xb8\x0c\x1a\xa0\x37\xee'
            b'\x56\xd4\x05\x17\xf9\xe5\x70\x1c\x4e\xaf\x01\xf6\xc7\xdd\x0a'
            b'\x87\xc3\x11\x0b\xfb\x0d\x70\x80\x85\x10\x0c\xe4\xce\x7f\x38'
            b'\x1c\xe3\x09\x28\x0b\xc0\x1e\xa0\x18\x77\x6b\x6a\x8e\x5b\x02'
            b'\x38\x1c\xe3\x29\x00\x7b\x0d\xb0\x0b\x17\x0c\xe4\x70\x2c\x34'
            b'\x0a\xc0\x4e\x83\xb0\xb3\xfc\x1f\x87\xc3\xb1\x70\xc8\x03\x3b'
            b'\x0d\x4a\x2f\x30\x10\x77\x6b\x6a\x8d\x5b\x01\x38\x1c\x87\xd0'
            b'\x2f\xd0\x67\x80\x11\x60\x47\xdc\xad\x71\x38\x1c\x75\x65\x87'
            b'\x0a\x23\x46\x94\x51\x60\x7b\xdc\xad\x71\x38\x1c\x75\x65\x7b'
            b'\x24\x8c\x1a\x35\x14\x80\x97\xe3\x6e\x8d\xc3\xe1\xa8\x2b\xdb'
            b'\xfd\x80\xa2\x29\xef\x8f\x6f\x65\x21\xc4\x02\x38\x16\x16\x51'
            b'\x84\x16\x0a\x63\x95\xa7\x34\x9f\x83\xd0\x25\xc0\x02\x4a\x28'
            b'\x5b\x22\x63\x73\x02\x02\xbc\x84\xf5\x05\x38\x1c\xf3\x03\x11'
            b'\x28\x14\xd0\xa7\x9f\x42\x0f\x1c\x40\xf7\xed\x25\x7a\xe2\x71'
            b'\xa8\x08\xc2\xc2\x66\x04\xc3\x4b\x50\x2e\x0a\xa2\xb0\x55\xec'
            b'\xb1\xe0\x78\x4a\x85\x3b\x1c\xb5\x40\x95\xe8\xc5\xcd\xb0\x63'
            b'\xbb\xcd\x0c\x5c\x70\xbb\xdd\x65\x86\x54\xd9\x0a\x65\x01\x10'
            b'\x7b\x20\x68\x2b\xb0\x32\xee\x96\x39\x1c\x55\x45\x15\x72\x39'
            b'\xfb\xef\x98\x66\x7e\x9b\x85\x5c\xf0\x4d\x12\xcf\x24\x00\x08'
            b'\xa3\x12\x41\x54\x44\xd1\x38\xb6\xa8\xb7\x02\x7d\x00\xbe\x00'
            b'\x08\x43\xaa\x3c\x0b\x5c\x1c\x4b\x0f\x39\x1c\xb5\x24\x66\x93'
            b'\xbf\x35\xb9\x98\x65\xad\x67\xd0\x95\x39\x8e\xb4\x6f\x8d\xec'
            b'\x7c\x30\x40\x5f\x6e\x0b\x7b\x86\x9f\x62\xa4\x58\xf7\xf3\x78'
            b'\xcf\x2a\x0c\x09\xe0\x87\x0a\x1e\x94\x80\xe7\x62\xed\x25\x87'
            b'\x63\x9e\x21\x18\x96\xb5\x9d\xce\x89\xdd\xaf\x27\x9b\x5c\x82'
            b'\x88\x19\x3b\x94\x96\x4d\x2d\xa1\xbb\xe5\x44\x7a\xda\xce\xe4'
            b'\xc5\xde\x9f\xb1\x67\xe8\x29\x94\xa8\x5e\x4d\x7b\xce\x83\xa0'
            b'\x00\x98\x9b\xaf\x1a\x6b\xd3\x53\xc0\x70\xdc\x9d\xe6\x70\xcc'
            b'\x17\x96\xb5\x9d\xce\x9a\x25\x57\xd2\x9a\x5c\x8a\x20\xa8\x46'
            b'\x04\x51\x81\x40\x0b\xa8\xda\x85\x41\x6b\x72\x29\x6b\x96\x5c'
            b'\xc9\xb2\xb6\xd3\xeb\xd5\xac\x61\xe0\x29\x05\xbe\x74\xe5\xf8'
            b'\xca\xc0\xca\x33\x08\x7d\x40\x6b\xdc\x1d\x57\x0b\xdc\x69\x60'
            b'\x47\xbd\x50\xac\xd9\x7f\x62\xf7\xeb\x49\x79\x59\x5b\x98\x38'
            b'\x18\x60\xd7\xd0\xe3\x0c\xe4\x5e\x06\x11\xba\x32\xc7\xd1\xd3'
            b'\x76\x26\x49\xaf\x95\x94\x97\xe5\xc4\xee\xd7\x33\x54\xd8\xcd'
            b'\x70\x71\x7f\xad\x7d\x02\x7d\xc0\x33\x95\xff\x1c\x14\x00\x61'
            b'\x1f\xf0\x02\x70\x6c\xdc\x1d\x58\x0b\x16\xfc\xc6\x8f\xa3\x6e'
            b'\x08\xb0\xac\xf5\x0c\xb2\xc9\x25\x80\x1d\xfc\x4f\xef\xbd\x95'
            b'\x7d\x23\xcf\x97\x67\x7e\xd8\x37\xfc\x2c\x03\xf9\xed\xac\x59'
            b'\x72\x05\x49\xaf\x95\x6c\x72\x09\xcb\x5a\x4f\x67\xa4\xf7\xe7'
            b'\xb5\x6e\xde\x73\xc0\xbe\xca\x7f\x0c\x58\x47\x69\x10\x32\x00'
            b'\x3c\x16\x77\xe7\x39\x1c\xcd\x8e\x6f\x52\x74\x65\x8e\x43\xc4'
            b'\xa0\x28\xbb\x86\x1e\x63\xdf\xc8\xf3\x80\x56\x62\x92\x50\x22'
            b'\xf6\x0c\x3d\xc5\xee\xa1\xc7\x01\x10\x31\x74\x65\x8e\xc7\x37'
            b'\xa9\x5a\x37\xef\xb1\x28\xcd\x60\x65\x46\x34\x00\x37\x5d\x05'
            b'\xbe\x87\x02\x8f\xb0\x10\x92\x83\x38\x1c\x35\xc4\x33\x09\xeb'
            b'\xed\x57\xbb\xdd\x37\x90\xdb\x3e\x36\xf3\x8f\x27\xd2\x88\xbe'
            b'\xdc\x36\x42\x2d\x82\x42\xda\xef\x18\xdb\x26\xac\x11\x45\xe0'
            b'\x11\x93\x47\x37\x5c\x61\x7f\x60\x0e\x7b\xc2\x6f\x29\xef\x0f'
            b'\x3a\x1c\x8e\x6a\x31\xd5\x02\x54\x27\xf8\x57\xcd\xe8\x05\x1e'
            b'\x1d\xff\x83\xc3\x05\x60\x1b\xf3\x75\x3b\xd0\x39\x01\x1c\x75'
            b'\x22\x8c\x4a\xe4\x83\x01\x10\x6b\x0d\x74\x64\x56\x22\x13\xc4'
            b'\x22\x88\x08\x1d\xe9\x95\x78\x92\x00\x81\x7c\xd0\x4f\x18\x95'
            b'\x6a\xd9\xb4\x67\x51\xb6\x8d\x57\x1a\x33\xfe\x5f\xd2\x4e\x3f'
            b'\xf0\x60\xdc\x1d\xe8\x70\x34\x33\x41\x54\xa0\x2f\xb7\x05\xd5'
            b'\x08\x41\x58\xde\x76\x16\x4b\xb2\xa7\x00\x82\xaa\xf5\xb9\x81'
            b'\xb0\x24\x7b\x0a\xcb\xdb\xce\x1a\xdb\x22\xec\xcb\x6d\x25\x88'
            b'\x6a\x1a\xae\xfc\x60\x64\xe8\x1f\x3f\x19\x8e\xed\x02\x6c\xb8'
            b'\x1c\xd6\x6d\x44\x81\x07\xb0\xe9\x82\xd2\x71\x77\xa4\xc3\xd1'
            b'\x8c\x28\xb0\x67\xf8\x29\x7a\xda\xce\xa4\x35\xb9\x94\x94\xdf'
            b'\xce\x69\x4b\xaf\xa2\x73\x68\x95\xdd\x06\x04\x3a\x33\xc7\xd2'
            b'\xd3\x76\x16\x29\xbf\x1d\x80\x91\xe2\x3e\xf6\x0c\x3f\x55\x0e'
            b'\x1b\xae\x09\x39\xe0\x7e\xa3\xb0\xe1\xca\x83\x3f\xf4\x8f\x78'
            b'\x9a\xf2\x30\xc2\x2e\xe0\x84\xb8\x3b\xd2\xe1\x68\x46\x04\x18'
            b'\x29\xee\x67\x73\xef\x3d\x9c\xba\xe4\x4a\x52\x5e\x2b\x69\xbf'
            b'\x83\xe3\xbb\x2e\x26\xec\xb0\x26\xbe\x67\x92\xe5\x81\x2e\x14'
            b'\xc2\x61\x36\xf7\xfe\x8c\xd1\xda\xc6\x00\xec\xc2\x3a\xf9\x0f'
            b'\xe1\x10\x01\x28\x3b\x2a\x77\x08\x3c\x8c\x13\x00\x87\x63\x4e'
            b'\xec\x1d\x7a\x1a\x10\x4e\x1a\x17\x0a\x3c\xb6\xcd\x27\xa0\x1a'
            b'\x31\x52\xdc\xcb\x8b\xbd\x3f\x63\xef\xd0\x53\xb5\x6e\xce\x43'
            b'\x22\xec\x3c\x7c\x33\xe2\x50\x01\x00\x3c\x21\xa7\x70\x2f\xf0'
            b'\x4e\x8e\x74\x12\x3a\x1c\x8e\x69\x62\xf7\xfa\x9f\x60\xb8\xb0'
            b'\x9b\x65\xad\xa7\xd3\x95\x39\xfe\x90\xc3\x40\xbd\xe5\xc3\x40'
            b'\xa3\xb5\x3f\x0c\x14\x01\xbf\x50\xc8\x99\xc3\xd2\xfe\x1c\x22'
            b'\x00\x37\x5f\x05\xeb\x36\x02\x70\x1f\x36\x5a\x68\x59\xdc\x9d'
            b'\xe8\x70\x34\x3b\xc3\xc5\xfd\x8c\xf4\xde\x8b\x6f\xee\x8f\xeb'
            b'\x38\xf0\x3e\xe0\x3e\x14\x6e\x78\xdb\xa1\xbf\x98\x6c\x86\x7f'
            b'\x8e\x09\xd6\x0b\x0e\x87\x63\xe6\xd8\x01\xae\x04\x51\x81\x42'
            b'\x30\x4c\x21\x18\x2e\x7b\xfb\xeb\x96\x0b\xe0\x61\x51\x9e\x97'
            b'\x09\x02\x0d\x8e\x10\x00\x13\x81\x1a\x86\x80\x7b\xe2\xeb\x32'
            b'\x87\xc3\x51\x25\x14\xb8\x47\x3d\x86\x74\x3a\x02\x70\xc3\xd5'
            b'\x20\x11\x08\xdc\x0d\xec\x8d\xbb\xf5\x0e\x87\x63\x4e\xec\x15'
            b'\xe1\x1e\x22\xd8\x70\xf5\x91\xbf\x9c\xd4\xc9\xa7\xf0\x34\xf0'
            b'\x50\xdc\xad\x77\x38\x1c\x73\xe2\x41\x85\xa7\x27\x5b\x6b\x4c'
            b'\x28\x00\xe5\xe7\x0e\x01\x77\x00\x2e\x8f\xb2\xc3\xd1\x9c\x84'
            b'\xc0\x8f\xd1\xc9\x13\xfd\x4c\x28\x00\x37\x96\x23\x85\x14\x7e'
            b'\x82\x2b\x1b\xe6\x70\x34\x2b\xdb\xb1\x63\x98\xca\xe9\xbf\xc3'
            b'\x99\x6a\x09\x80\xda\x04\x21\x3f\x8b\xfb\x2a\x1c\x0e\xc7\xac'
            b'\xb8\x47\x60\xf3\x54\x3b\x0d\x93\x0a\x40\x21\x04\x23\x14\x54'
            b'\xf8\x11\x36\x8e\xd8\xe1\x70\x34\x0f\xa3\xc0\x8f\x14\x0a\x53'
            b'\xa5\x1a\x9d\x54\x00\xfe\xfe\x1a\x40\x41\x6c\x54\xe0\x13\x71'
            b'\x5f\x8d\xc3\xe1\x98\x11\x4f\x08\xfc\x02\xe0\xa6\x2b\x27\x7f'
            b'\xd2\x94\xa1\xbe\x91\x42\x9b\xcf\x6e\xe0\x16\x5c\x5e\x4d\x87'
            b'\xa3\x59\x50\xe0\x96\xd1\x1c\x7b\x8e\x56\x12\x61\x4a\x01\xb8'
            b'\xf9\x2a\x18\xb2\x87\x97\x6e\xc5\x39\x03\x1d\x8e\x66\x61\x3b'
            b'\x70\x6b\x26\x03\x37\x5e\x31\xf5\x13\xa7\x7b\xd8\xe7\x29\xe0'
            b'\xc7\x71\x5f\x95\xc3\xe1\x98\x16\x3f\x56\xe1\xe9\xe9\x98\xec'
            b'\x47\x15\x80\x72\xf2\x80\x22\xf0\x3d\x60\x20\xee\x2b\x73\x38'
            b'\x1c\x53\xd2\x0f\x7c\x4f\x94\xe2\x54\x6b\xff\x0a\xfe\xd1\x9f'
            b'\x52\x46\xf8\x35\xca\x2f\x80\xab\xe2\xbe\xc2\xb8\x11\x18\xcb'
            b'\xdc\xe2\x52\x0d\xce\x17\x64\xdc\x9f\x4d\xcd\x2f\x80\x5f\x4f'
            b'\xf7\xc9\xd3\x12\x00\x2f\x80\x20\xc9\xa0\x28\xdf\x06\x2e\x03'
            b'\x32\x71\x5f\x65\x3d\xa9\x0c\xf8\x00\x25\x44\xd1\xb2\x3f\x34'
            b'\xd2\x80\x28\x2a\xcd\x87\x9b\xc6\x01\xe4\x34\x20\x6a\x6e\x5f'
            b'\x77\x0e\xf8\x0e\x86\x21\xf2\xd3\x7b\xc1\xb4\x04\xe0\x8b\x6f'
            b'\xb3\x79\x02\x54\xb8\x53\x94\x07\x81\xd7\xc5\x7d\xa5\xf5\xa2'
            b'\x44\x44\xbf\x16\x39\x40\x81\x21\x4a\xe4\x35\x22\x2c\x17\x71'
            b'\x94\xa2\x40\xc9\x0d\xff\xf9\x80\x00\x11\x4a\x21\x0a\x9b\x59'
            b'\xd0\x1f\x10\xe5\x4e\x8d\x60\xc3\x7f\x9a\xde\x0b\xa6\xbf\x04'
            b'\x88\x40\x7c\xf6\x63\xad\x80\x0b\x80\x64\xdc\x57\x5b\x4b\x14'
            b'\x65\xaf\xe6\xd9\xaa\xc3\xf4\x53\xa4\x34\xd1\xcc\x50\x0e\x97'
            b'\x74\xcc\x1f\xc6\x0f\x7e\x51\x7b\x32\xb6\x49\x28\x02\xff\x5c'
            b'\x52\xf6\xa7\xbd\xe9\xbf\x68\xda\x02\xb0\xe1\xea\xb1\x6c\x41'
            b'\xb7\x00\x1f\x00\x2e\x8c\xfb\x8a\x6b\x81\x00\x21\xca\x66\x1d'
            b'\x62\x8f\xe6\x29\x12\x8d\x5b\xeb\xab\x1b\xf0\xf3\x91\x89\x72'
            b'\xf6\x2b\xa8\x07\xda\x3c\xe6\xc0\x43\xaa\xdc\xea\x1b\xf8\xc2'
            b'\xe5\xd3\x7f\xd1\xf4\x2d\x00\x20\x0a\x21\x91\x66\x77\x58\xe2'
            b'\x7f\x03\xe7\xd2\x4c\x56\xc0\x0c\xbe\xc8\x12\x11\xdb\x75\xf4'
            b'\xe0\xcb\x54\x51\x55\x4c\x32\x85\xd7\x92\xc5\x78\x89\x79\xe1'
            b'\x2d\x72\x80\x46\x4a\x30\xd4\x8f\x86\xe3\x92\xe5\x29\x04\xad'
            b'\xca\x81\xd7\xe4\x08\xda\xa2\x66\x10\xfd\x22\xf0\x4d\x2f\xc1'
            b'\xee\x60\x86\x85\xfd\x66\x24\x00\x37\x5f\x03\xeb\x36\x01\xc2'
            b'\x0f\x51\x7e\x9f\x26\xb2\x02\x66\x3d\x5e\x55\x31\x99\x16\x3a'
            b'\xce\x3c\x9f\xce\x73\x5e\x4b\x66\xe5\x49\xf8\xd9\x36\x30\xa6'
            b'\x19\x6e\x0c\xc7\x14\x88\x31\x0c\x3d\xfd\x1b\xb6\x7e\xeb\x6f'
            b'\x09\x87\x07\x2b\x55\x3b\x29\x76\x87\xec\xbe\x7c\x94\xa1\x53'
            b'\x8a\xcd\x92\x16\xf7\x41\x55\x6e\x89\x4a\x70\xf3\xd5\x33\x7b'
            b'\xe1\x8c\x04\x00\xc0\x78\x50\xca\xb1\xcb\x4b\xf0\x75\xe0\x1c'
            b'\xa0\xe6\xe5\x4c\xab\xc1\xac\xc6\xaa\x2a\xa9\x65\x2b\x59\xf1'
            b'\x8e\x0f\xd2\x75\xee\x6b\xf1\x32\xad\x80\x4e\x58\xe8\xd1\xd1'
            b'\x5c\x88\x08\xc1\xe8\x30\xbd\x0f\xdc\x4d\x38\x3c\x00\x62\x05'
            b'\x3d\x68\x8b\xec\xe0\x3f\xad\xd8\x2c\x02\x5f\x00\xfe\x49\x7d'
            b'\x76\x9b\x59\x94\xf5\x9d\xb1\x00\xdc\xf0\x16\x58\x77\x1b\xa0'
            b'\xdc\x82\xf0\x1e\xe0\x8d\x71\xf7\xc0\x51\x91\x59\x58\x00\xaa'
            b'\xa4\x96\xae\xe0\xb8\x0f\xac\xa5\xfd\x15\xaf\xb6\x3f\x8a\x5c'
            b'\x6e\x94\x79\x83\x08\x03\x8f\xdd\xcf\xe0\x13\x0f\x32\xe6\xe1'
            b'\xf1\x95\xfd\x97\xe4\x18\x3a\xb5\x69\x06\x3f\xd8\x74\xdf\xb7'
            b'\x98\x10\x6e\xbc\x66\xe6\x2f\x9e\x95\x81\x13\x00\x46\xd8\x0f'
            b'\xfc\x03\x36\x73\x50\x63\x33\x63\xdf\x9d\x62\x92\x69\x7a\xae'
            b'\x7e\x9f\x1d\xfc\x07\x0b\xba\x39\xe6\x03\x22\x84\xb9\x51\xfa'
            b'\x7e\x7d\x17\x61\x7e\x64\xcc\xf4\x1f\x5e\x5d\xa2\xff\xec\x42'
            b'\x33\xf9\x77\x86\x80\x7f\xf0\x84\x03\xc1\x2c\x77\x2b\x66\x25'
            b'\x00\x7f\x7b\x95\xad\x34\x20\xca\xed\xd8\x83\x42\x8d\xcd\x0c'
            b'\x2d\x00\x8d\x94\xd6\x53\xce\xa2\xfb\xfc\x37\xc4\xdd\x72\x47'
            b'\x0d\x10\x11\xf2\xbb\xb6\x32\xfc\xc2\x13\x48\xd9\xf4\x8f\xd2'
            b'\x4a\xef\x79\x05\x82\x96\xa6\xda\xe9\xb9\x45\x84\x4d\x0a\xfc'
            b'\xed\x0c\xd7\xfe\x15\x66\xed\xe2\x38\x6e\x1f\xa8\x30\x02\x7c'
            b'\x99\x79\x76\x52\x50\x3c\x8f\x8e\x57\x5d\x88\xdf\xda\xe9\x66'
            b'\xfe\x79\x89\x30\xfc\xc2\x13\x94\x06\xfb\x40\x04\x51\xc8\x1d'
            b'\x13\x90\x5b\x55\x42\x9a\xe7\xeb\xde\x0e\x7c\x45\x95\xd1\x33'
            b'\xe6\x50\xc6\x77\xd6\x02\xf0\xf1\xf7\x8f\xfd\xf3\x01\xe0\x9f'
            b'\x69\x78\xdd\x9c\xba\x79\x63\xfb\xbd\xaa\xf8\x2d\xad\x64\x4f'
            b'\x38\xf5\xe8\x97\x24\xe2\x1e\x8d\xf8\x38\x0a\x51\xa9\xc8\xe8'
            b'\xb6\x17\xd0\x20\x18\xfb\xee\x47\x8e\x2f\x11\x66\x9a\x66\xf6'
            b'\x57\xe0\x9f\x43\xc3\x03\x2a\xf0\xfe\x4b\x67\xff\x46\x33\x76'
            b'\x02\x8e\x67\xc3\x95\xb0\x6e\x23\x81\xc0\x3f\x29\x5c\x09\x9c'
            b'\x19\x77\xcf\xcc\x86\x72\xb9\xf6\x31\x24\x91\x22\xd1\xb9\xe8'
            b'\x88\xc9\x5f\x44\x90\x71\x37\x58\x69\xa8\x9f\xb0\x58\x68\x96'
            b'\x9b\x66\x41\x60\x12\x09\x92\xed\x9d\x88\x78\x63\x67\x36\xc6'
            b'\x23\x22\x04\xf9\x51\x8a\xfb\x76\x8d\x89\x45\x94\x52\xf2\x3d'
            b'\x21\x2a\x34\x8b\x05\xf0\x38\xf0\x0d\x2f\x22\xdc\x30\x8d\x13'
            b'\x7f\x53\x31\x27\x01\xa8\x90\x2c\xf2\x7c\x21\xc9\xd7\x80\xff'
            b'\x41\x93\x6c\x0b\x8e\x47\x38\xf4\x8b\x17\x23\x88\x97\xa0\x32'
            b'\xb2\x7d\xdf\x27\x99\x48\x90\x48\x24\xf0\x3c\x0f\x41\xd9\xfd'
            b'\x8b\x1f\xf3\xe2\xf7\xbf\x41\xa1\x77\x2f\xb5\x2c\xea\xee\x98'
            b'\x01\x0a\x89\xb6\x4e\x4e\x78\xc7\xfb\x39\xe6\xb2\xb7\x23\x66'
            b'\x02\x03\x57\x84\x82\x06\x44\xc3\x03\x63\xaf\x89\x12\x4a\xa9'
            b'\x23\x6c\x96\xc1\x9f\x57\xf8\x6a\xa7\xc7\xf3\x7d\x55\xd8\x94'
            b'\x9a\xb3\x00\x6c\xb8\x12\xd6\x6f\x02\x03\xdf\x89\x94\x37\x62'
            b'\xab\x0a\x37\x14\x32\xf6\xc7\x14\x4c\x54\x36\xc9\x18\x32\xa9'
            b'\x14\xe9\x74\x1a\xaf\x7c\x33\x89\x08\x85\x81\x5e\x5e\xfa\x3f'
            b'\xff\xc4\xe0\x73\x8f\x21\x66\x06\x81\xd7\x8e\x9a\x53\xd8\xbf'
            b'\x8b\x6d\xb7\x7c\x8b\x9e\xd7\x5c\x4a\xaa\x73\xd1\x11\x31\x1b'
            b'\x22\x06\xa3\x4a\x58\xc8\x1d\xbc\x27\x0c\x84\xe9\xe6\x18\xfd'
            b'\xc0\x46\x85\xef\xf5\x87\x70\xf3\x1c\x67\x7f\xa8\x92\x05\x90'
            b'\x48\x40\xa1\x40\xbf\x08\x37\x01\xe7\x01\xab\xe2\xed\xa3\x43'
            b'\x99\xf1\x57\xab\xe0\xfb\x1e\xed\xad\x6d\x24\x13\xfe\x91\xef'
            b'\xa5\x6a\x43\x47\x95\x09\xcd\xcc\xa3\x21\x1c\xb9\x56\xad\xf6'
            b'\xed\x77\x84\xde\xa9\xce\xaa\xad\x4d\x87\x62\xa3\xd5\x44\x26'
            b'\xbd\xda\x26\xee\x85\xad\xc0\x06\x0f\xfa\x47\xab\xf4\x86\x55'
            b'\x11\x80\xff\xfe\x26\x58\xbb\x09\x42\xe1\x7e\x2f\xe2\x6b\xc0'
            b'\xe7\xaa\xf5\xde\xd5\x60\x5a\xd6\xf9\xd8\x93\x14\x31\x42\x6b'
            b'\x36\x4b\x2a\x99\x44\xf5\xb0\x0d\x56\xd5\xb2\x99\xf9\x07\xbc'
            b'\xf4\x83\xff\x9f\xd2\x50\xff\x8c\x5b\xa3\x51\x48\xb1\xbf\x77'
            b'\x2c\xb0\x48\x10\xd2\xc6\xc3\x20\x73\xbe\x39\xc7\x1f\x6b\xad'
            b'\x0c\x78\x31\x1e\xc9\xce\xee\xb2\xb5\xd2\xc4\xb7\xff\x34\xae'
            b'\x3e\xdd\xbd\x84\x13\xdf\xf5\x21\x92\x6d\x9d\x13\xee\xe0\x28'
            b'\x8a\x78\x1e\x7e\x3a\x73\x70\xe9\x16\x81\x97\x17\x4a\x71\x37'
            b'\x7f\x6a\x02\xe0\x6b\xc0\x03\x0a\x7c\xb9\x0a\xb3\x3f\x54\x71'
            b'\x90\xde\x74\x05\xac\xdb\x48\x84\xf0\x0d\x94\xcb\x80\x37\xc5'
            b'\xd1\x4b\xb3\x41\x39\xb8\x0b\xa0\xd8\x6d\x21\x33\xc5\xf6\x9f'
            b'\x18\xc3\x31\x6f\x7c\x1b\x4b\x5f\xfd\x3a\xa2\x52\x91\x19\x39'
            b'\x00\x44\x28\xf4\xee\xe5\xa1\xcf\x7d\x94\xc2\x81\xbd\xa8\xd8'
            b'\xc1\xff\xda\xec\x09\x64\xa4\x3a\x5f\x47\x4e\x03\xee\x1d\x79'
            b'\x89\x5c\x14\x20\xaa\x24\x3b\xbb\x39\xef\xb3\x5f\x25\xd5\xbd'
            b'\x74\xde\x6f\x6b\x7a\xa9\x14\x89\xb6\xce\xa9\x9f\x93\x48\x92'
            b'\xec\x5c\x0c\x3c\x0b\x02\xa6\x24\x24\x06\x3c\x72\x2b\x1a\xda'
            b'\x0f\x70\x37\xca\x37\x10\xa2\xb9\x3a\xfe\xc6\x53\xdd\x59\xda'
            b'\x00\x21\x7b\x10\x6e\x00\x5e\x01\xf4\xd4\xb3\x87\x66\x8b\x1a'
            b'\x08\x13\x6a\x4d\x73\x20\x2c\x16\x28\xf4\xee\x25\xbb\x62\xd5'
            b'\xa4\x13\xa6\x88\x21\xd9\xb9\x68\xec\x35\xd3\xef\xa3\x72\xea'
            b'\x29\x53\xf1\x52\x0b\x06\x21\x23\x3e\x2d\x26\xc9\xdc\x67\x68'
            b'\x81\x08\xcc\xd8\x01\x66\x45\x8c\x47\xaa\x7b\x29\x99\xa5\xcb'
            b'\x6d\xae\xf7\x79\x8c\x72\x94\xa8\x4d\x55\xbc\x74\x0b\x2d\x3d'
            b'\x2b\xc7\xba\xda\x14\x85\xf4\x6e\x8f\xa1\x53\xe3\x6e\xfd\xa4'
            b'\xec\x02\x6e\x10\xd8\x1b\x56\xf9\x70\x52\x55\xdf\x6e\xc3\xe5'
            b'\xe5\xd9\x54\xb9\x1b\x1b\x20\xd4\xe0\x56\x15\xd6\x0b\xec\x41'
            b'\xbe\xa5\x6c\xea\x8b\x10\x8c\x0c\x32\xf0\xfc\x13\x1c\x75\x66'
            b'\x57\x45\x35\x9a\xd1\x83\xa8\x72\x83\xea\xf8\x26\x8c\xfd\xab'
            b'\xf2\x9b\xd9\x3e\x0e\xfd\x73\xdc\x27\xa8\x42\x34\xf3\xf6\x36'
            b'\xdb\x63\x3a\x16\x8e\x49\x26\x69\x3f\xe1\x54\x8c\x9f\xb0\x5f'
            b'\x79\x04\xd9\x97\x12\x78\xb9\xd9\x1c\x1a\xa9\x39\x25\xe0\xcb'
            b'\x0a\xf7\x44\x02\x37\xcf\xe0\xac\xff\x74\xa8\xfa\x61\xc7\x9b'
            b'\xae\xb2\xa1\xd6\xa2\x7c\x0d\xb8\xad\x3e\x7d\x34\x0d\xa6\xf8'
            b'\x62\x43\x5f\x19\xe9\x3c\xb8\xd6\x8f\xc2\x80\xbd\x0f\xfe\x8c'
            b'\x62\x39\x52\xcc\x31\xcf\x50\xa5\xf3\xb4\xb3\x49\x76\x76\x5b'
            b'\x11\x17\xc8\xec\xf4\x69\xd9\x96\x68\xc4\x04\x20\xb7\x09\xfc'
            b'\x4f\x81\x70\x3a\x59\x7e\x67\x4a\x6d\x4e\x3b\xa7\x41\xe1\x00'
            b'\xf0\x37\xc0\x73\x35\xed\x9e\x2a\xa0\x02\x03\x4b\x43\x4a\xc9'
            b'\xb2\xd3\x4c\x0c\xbd\x4f\x3e\xcc\xae\x5f\xdc\x1e\x77\xd3\x1c'
            b'\x35\x40\x55\x69\x3d\xf6\x04\xba\x4e\x3b\xdb\x5a\x0d\x02\x26'
            b'\x2f\x74\x3d\x98\xc2\x1f\x69\x28\x2b\xe0\x59\x94\xbf\x56\x38'
            b'\x40\x8d\x0e\xa2\xd6\x44\x00\x36\x5c\x66\x4d\xd0\x1d\xfb\x79'
            b'\x18\xb8\x01\x26\xaf\x4f\x5e\x1f\x74\xca\xef\x54\x14\x06\xbb'
            b'\x23\x06\x97\x44\xd6\x09\x24\x42\x58\xc8\xb1\xf9\x5f\xff\x91'
            b'\xfd\xbf\xb9\xcf\x9e\x15\x77\x96\xc0\xfc\x41\x15\x3f\x93\x65'
            b'\xf9\xeb\xaf\xc4\xcf\xb4\xda\x65\x83\x40\xeb\xe6\x24\x9d\x8f'
            b'\xa4\x1b\x65\xa3\x64\x18\xd8\xd0\xd7\xc5\x6f\x54\x60\xc3\x2c'
            b'\x8e\xfa\x4e\x87\x9a\xe5\x3b\xb9\xe9\x2a\x58\xb9\x18\x04\xbe'
            b'\x0b\x7c\x8b\xb8\xbb\xf5\x28\xe3\x37\x48\x2a\xbb\x4e\x2a\x51'
            b'\x4a\xd9\x78\x70\x11\xc3\xe8\xee\xed\x3c\xf1\x95\xbf\x64\xc7'
            b'\xdd\x3f\x24\xcc\x8f\x22\x9e\x87\x18\x83\xc8\xec\x1f\x98\x4a'
            b'\x0c\x40\x3d\x05\xa5\xfc\x99\x46\xe6\xd4\xf6\xf9\xf4\x00\x61'
            b'\xc9\xb9\xaf\x65\xf1\x39\x17\x8d\x05\x0b\x49\x00\x8b\xef\x4b'
            b'\xd3\xf6\x4c\x32\x6e\x2b\x40\x81\x6f\x22\xfc\x4b\x57\xbf\xdd'
            b'\x61\xab\x15\x35\xdd\xab\xbf\xd1\x9e\x15\x18\x05\xbe\x00\x9c'
            b'\x4c\x5c\x5b\x83\x95\xf1\x36\x45\xc8\xae\x28\xf4\xf6\x04\xec'
            b'\x3a\xd1\x63\xe5\xb3\x09\x9b\x11\x56\x84\x91\x9d\x5b\x79\xf2'
            b'\xcb\x7f\xc5\xde\x5f\xfd\x84\xa5\xaf\xb9\x94\xb6\xe3\xd7\x90'
            b'\x68\xeb\x28\xdf\x44\xb3\x69\x8b\xdd\x06\xd4\x28\x44\xaa\xb0'
            b'\xef\x7f\xf4\x4b\xb7\x71\x07\x85\xde\xbd\xf6\x07\xf3\x7c\x1b'
            b'\x70\x26\x88\x31\x2c\xbf\xe4\x0a\x7a\x1f\x7f\xc8\xc6\x73\x88'
            b'\xe0\x0f\x19\x7a\x6e\x6f\x01\x81\xa1\x35\xb3\x48\xb1\x53\x1d'
            b'\x7e\x82\x70\x03\xca\x68\x35\xb7\xfc\x26\xa2\xe6\xc1\x3a\xc6'
            b'\x40\x18\xf1\xb2\xc0\x67\xb0\x11\x82\xa7\xd4\xfa\x33\x0f\x47'
            b'\x0c\x78\x49\x3d\xea\x96\x84\x7a\xb0\xfd\xd4\x22\xc9\xbc\xb0'
            b'\x6c\xab\x3f\x66\x09\x04\xa3\xc3\xec\xfc\xf9\x46\xf6\xdc\x7f'
            b'\x37\x7e\x4b\xab\xf5\x1e\xcf\x7a\x86\x38\x18\x08\x34\xd3\x65'
            b'\x45\x45\xc3\x66\xf6\x22\xa1\xd8\xdf\xcb\x43\x9f\xfb\xe8\x02'
            b'\x08\x04\x9a\x29\x02\x1a\x11\xe4\x46\x0e\x7e\x17\x02\xc9\x5e'
            b'\x8f\xe5\x3f\xca\xe2\x8d\x0a\xfd\xaf\xaa\x7b\x82\x90\xe7\x80'
            b'\x4f\x4b\xc4\xcb\x61\x1d\xa2\xcc\xeb\x72\x69\x6b\x37\xc1\x86'
            b'\x2b\x60\xfd\x46\x7e\x17\xf8\x0a\xb0\xa8\x1e\x9f\x3b\xfe\x2a'
            b'\x8b\x03\x86\xe1\x1d\x89\xa3\x4f\x80\x02\x89\xbc\xb0\xea\xa9'
            b'\x24\x3d\x2f\xfa\xf8\x25\x19\xe7\x19\xd6\x59\x87\xff\x1e\xfa'
            b'\x11\x07\x43\x81\x15\x68\x31\x09\xde\xdc\xba\x9a\x16\x93\x98'
            b'\xf0\x9d\xc7\x47\xf7\xf9\x62\x48\x4c\x72\xd2\xad\xf2\xdc\xd1'
            b'\xa8\xc4\x9d\xc3\x2f\x30\x3a\xbe\x6a\xd1\x42\x09\x05\x9e\x21'
            b'\x13\x85\x65\x83\xdd\x1a\x2c\x2c\x09\xd9\xf2\x81\x41\x4a\x1d'
            b'\x75\xcb\x0c\xdc\x0b\x7c\xbc\x6f\x17\xff\xd2\xd9\x63\x97\xd1'
            b'\xb5\xa6\x2e\xe1\xba\x37\x5d\x01\xe6\x36\x10\xe5\xfb\x2a\xac'
            b'\xc1\x5a\x03\x89\x7a\x7c\x36\x60\x63\xfb\x5b\x14\x3f\x13\x51'
            b'\x1a\x35\x47\x7d\x6e\x29\xad\xbc\x74\x56\x81\xc1\xc5\x21\xcb'
            b'\x5f\x48\xd0\xd6\xeb\xe1\x97\xe0\xa0\x5e\xd6\x67\x4a\xa8\xcc'
            b'\xf8\x03\x61\x9e\x17\x8b\x7d\xec\x2c\x0d\xd2\xe6\xa5\x38\x2e'
            b'\xd9\x49\x8f\xdf\x46\x4a\x7c\xa6\x2f\x47\x32\xf3\xa0\xa5\x85'
            b'\xc2\x24\x1d\xa8\xa6\xae\x75\x01\x8a\xc0\x97\x88\xf8\xf7\xae'
            b'\x1e\xd8\x50\xa7\x0a\x9c\x75\x8b\xd7\xbf\xf1\x2a\x58\xb7\x91'
            b'\x92\x2a\x7f\x2f\xc2\x49\xc0\xfb\xa8\xa3\x71\x65\x7c\x25\xbd'
            b'\x28\x24\x28\x18\xf4\x68\x5b\x2a\xe5\xe0\xa0\x7d\xab\x02\xfa'
            b'\x97\x86\xb4\xef\xf7\xe8\xdc\xeb\x91\x1d\x30\x24\x73\x82\x17'
            b'\xc8\xec\x67\x04\xb1\xb3\x4b\xa2\x20\x93\x86\x9d\x56\x06\xfe'
            b'\x60\x54\x60\x4b\xb1\x9f\x6d\xc5\x3e\x86\xa3\x62\xf9\x67\x79'
            b'\xf6\x04\xc3\x2c\xf1\x5a\x38\x2e\xd9\xc5\xf2\x44\x1b\xe9\x72'
            b'\x08\xf1\xa4\x87\x5f\xc4\x8a\x9a\x1a\xdc\x0a\x60\x2a\x04\x8c'
            b'\x67\x77\x04\x82\xf6\x88\xfd\x17\xe7\x08\x5a\xeb\x32\xfb\x2b'
            b'\xf0\x2f\xc0\xdf\x61\x28\xd5\x7a\xdd\x7f\xd8\x25\xd7\x97\x72'
            b'\x75\xa1\x55\xd8\x83\x0d\x35\xf4\x6f\x4e\x80\xc2\xe8\x3e\x8f'
            b'\xdc\x01\x7f\x46\x5f\x6a\x25\x51\x84\x5f\x12\x4c\x38\xb7\xa4'
            b'\x11\x0a\xa4\x72\xc2\x19\xf7\x66\x48\xe6\xec\xf2\xe2\xe0\x12'
            b'\x20\x89\xa2\x0c\x47\x05\xb6\x16\xfb\xd9\x5a\xec\x67\x28\x2a'
            b'\x4c\xe8\xbb\x54\x14\x0f\xc3\x22\xdf\x0a\xc1\x31\x7e\x1b\x19'
            b'\x93\x00\x84\xd1\xa8\x78\x70\x09\xa0\x50\xcc\x28\x4f\xbe\x36'
            b'\x47\x21\xa3\xce\x06\x98\x8c\x72\x27\xa7\x17\x85\x64\xba\x43'
            b'\xa2\x84\xda\x0c\x41\xf5\xe1\x0e\x94\x0f\x23\x6c\xab\xe7\xe0'
            b'\x87\xf8\x4e\xec\x6d\x03\xd6\x01\x8b\x81\x57\xd7\xed\x53\x05'
            b'\x32\x8b\x43\x40\xc8\xf7\x7a\xd6\x12\x98\xc6\x88\xa8\x0c\xf8'
            b'\x20\xa1\x73\xae\x85\x54\xb9\xa5\x74\xdc\x4a\xa4\xd2\x84\xe1'
            b'\xa8\xc0\xb6\x62\x3f\x5b\x4a\x7d\x0c\x86\x07\x07\xbe\x94\x5f'
            b'\xa8\x06\x4c\x54\x16\x24\x84\x08\x65\x6f\x30\xcc\x81\x60\x94'
            b'\x17\xbd\x0c\xc7\x27\x3b\x59\x99\xe8\x38\xe4\x3d\x2b\x9f\x55'
            b'\xc8\x28\x85\x16\x27\x00\x53\xa1\x0a\x21\x60\xb2\x8a\xf1\xeb'
            b'\x96\x1e\xec\x41\x60\xad\xc2\x36\x2f\x86\x22\x24\x75\xcf\x66'
            b'\xf1\xcb\x6f\xc3\x6b\xde\x07\xa9\x80\x7d\x91\xe1\x59\xe0\x12'
            b'\xea\xe8\x14\x14\x01\xbf\x25\xc2\x4b\x40\x14\x08\x51\x28\x75'
            b'\xcd\xe8\x23\x62\x2d\x89\x9e\xcd\x09\xfc\x92\xd8\x34\x76\x08'
            b'\x21\xca\x53\x85\xbd\xbc\x5c\xea\x27\xaf\xe1\xd8\xc0\x17\xb5'
            b'\x31\x0a\xfb\x56\x85\xec\x5a\x5d\x22\xf2\x21\x99\x2f\x2f\x43'
            b'\xb0\x5b\x95\x0a\x8c\x6a\x91\x3d\xc1\x08\xfb\x82\x61\xf2\x1a'
            b'\x70\x20\x1c\x1d\x2b\x75\x1d\x26\x60\xcf\x89\x25\x02\x57\xd1'
            b'\x6c\x4a\x04\x7b\x4f\xf8\x49\xc5\xaf\x4f\x82\x90\x17\x14\xfe'
            b'\x9f\x74\xc0\x83\xf9\x44\xf5\xe3\xfc\xa7\x7b\xcd\xb1\xb0\x6e'
            b'\x13\xb4\x1c\x0f\xa3\x2f\xf1\x4e\xec\xce\x40\xdd\x4f\x0e\x46'
            b'\x25\xa1\x34\x62\x28\x8d\x08\x61\xd1\x10\x05\x73\x7f\x4f\xc0'
            b'\xfa\x10\x82\xc9\x02\x0e\x20\x35\x2a\xbc\xea\xce\x16\x52\xa3'
            b'\x87\x86\x9d\x8e\xd7\x21\x51\x6b\x71\xf4\xf5\x84\xec\x3e\x31'
            b'\xa0\x7f\x69\x40\xe8\x83\x5f\x82\xf6\x03\x1e\xcb\x5f\xf6\xe9'
            b'\xdc\xe9\xe3\x8f\x1e\xdc\xbe\x3a\xfc\x3d\x2a\x3f\x28\x64\x95'
            b'\xc7\x2e\x1f\xa5\xd0\xd2\x3c\xa5\x6e\x63\x43\x21\xd1\x1a\x91'
            b'\xed\x09\x98\x6d\xa8\xc7\x34\xd9\x0d\x7c\xac\xa5\xc4\xf7\x73'
            b'\xbe\xf5\x91\xc5\x41\xac\x13\xc2\xda\xdb\x6c\xe9\x3d\x63\xf8'
            b'\x03\x6c\xc8\x70\x7d\xb7\x07\x2b\x3d\x10\x81\x46\x72\xf8\x21'
            b'\xbd\x59\xbf\x5f\x54\x82\xa1\x97\x13\x13\x8b\xc0\x14\x02\x00'
            b'\x76\xe0\x87\x3e\x0c\x2c\x09\xd9\x75\x52\x89\xbe\x9e\x90\x20'
            b'\xa1\x87\xe6\x2c\x4c\x28\x9d\xcb\x03\xda\xf6\x7b\x74\x3c\x9a'
            b'\xa2\xed\xd9\x04\xfe\xb0\x39\x78\x3d\xe3\x51\x28\x75\x44\x6c'
            b'\xfe\x83\x41\x4a\xed\x4d\x51\xe8\x32\x7e\xc4\x3a\x8d\x6b\xc8'
            b'\x01\xe0\x7a\x94\xff\x55\xed\xf3\xfd\x33\x25\xd6\xac\x3d\x37'
            b'\x5d\x05\xeb\x36\x11\x29\x7c\x53\x94\x14\xf6\xf0\x50\x57\x5d'
            b'\x1b\x51\x9e\x32\xc5\xab\xd2\xfa\xb8\x92\x80\x70\x86\x6f\x26'
            b'\x0a\xa1\x81\xa1\xc5\x21\xbb\x4f\x0a\x38\xb0\x22\xa0\x94\xb2'
            b'\x03\xff\x70\xa7\xa3\x00\xa4\x95\x91\x13\x4b\x8c\x1e\x1b\xd0'
            b'\x7f\x8e\x15\x82\xf6\x67\x92\xf8\x83\x13\x0b\x81\xf1\x15\x93'
            b'\x68\x9a\xb4\xd7\xf3\x99\x7e\xe0\xb3\x02\xdf\xd4\x98\x07\x3f'
            b'\xc4\xe0\x03\x38\x9c\x5f\x7e\x1b\x2e\x79\x2f\x91\x11\x1e\x55'
            b'\xc8\x01\x17\xd1\x84\x99\x85\xc7\xa3\xa1\x50\xe8\xf7\xd0\x68'
            b'\x62\x15\x30\x91\xb0\x78\xbb\x4f\x2a\x57\x0e\x06\xf2\x6c\x61'
            b'\x8a\x9d\xe7\x14\xd8\x72\x6a\x89\x81\x45\x21\xea\x4d\xae\x21'
            b'\xe2\x41\xba\x33\xb2\x26\xaa\x81\x62\x57\xc4\xc8\x49\x25\x46'
            b'\x8e\x0f\xd0\x04\xf8\xc3\x06\x2f\x5f\xf6\x11\x44\x50\x58\x16'
            b'\xd2\x7f\x76\x01\xad\x5f\xe4\x85\x63\x62\x86\x80\xbf\x56\xbb'
            b'\x03\x56\xd7\xed\xbe\xc9\x88\x5d\x00\x00\xee\xfb\x36\x5c\x74'
            b'\x2d\xa1\xc0\x6f\xb1\xb9\xcf\x2e\x60\xce\xfe\xf6\xf8\xd0\x68'
            b'\x6a\x01\xd0\x24\x98\xb6\x88\x96\x51\x43\xd0\x11\x71\xe0\xe2'
            b'\x1c\xfb\x2e\xcb\x31\x7a\x4a\x11\xd3\x16\x41\x24\x76\xf9\x30'
            b'\x59\x9c\x40\x45\x00\xca\xdf\x9e\x94\xad\x98\xa0\xa3\x2c\x04'
            b'\x27\x94\x88\xd2\x8a\x44\x42\xbe\x27\x64\xff\x25\x79\x0a\xcb'
            b'\x5c\x61\xd3\x98\x19\x01\xbe\x20\xf0\x77\x02\x85\x46\x18\xfc'
            b'\xd0\x60\x4e\xe1\x75\xb7\x81\x42\x8b\x08\x6b\x81\xf5\x40\x36'
            b'\xee\x36\xcd\x86\xa8\x24\x0c\x6c\x49\x10\x95\x0e\xed\x5e\x31'
            b'\x90\xc8\x46\xa4\x3a\x43\x12\x19\x25\x91\x17\x9b\x8e\xac\x25'
            b'\x3a\x24\xd0\x5f\x23\x28\x8d\x18\x0a\xfd\x1e\xa5\x11\xc3\xe1'
            b'\x79\x49\x4d\x42\xe9\x38\xbe\x64\x4d\xfa\x89\xa8\x24\xba\xcc'
            b'\x09\xea\xd9\xba\x77\xce\xf4\x8f\x95\x51\xe0\x26\x51\x6e\x00'
            b'\x46\xe3\x72\xf8\x4d\x44\x43\x58\x00\x15\x7e\xf9\x1d\xb8\xf8'
            b'\xbd\x94\xc4\xee\x8d\x96\xb0\x31\x02\x4d\xb7\x1c\x38\xdc\x02'
            b'\x10\x03\xc9\xd6\x88\x96\xa5\x01\x99\x45\x21\x7e\x5a\x11\x63'
            b'\x2b\xd2\x68\x72\xa2\xea\x35\xe0\xa5\x94\x64\x5b\x64\xb7\xa3'
            b'\xf4\x50\x8b\xe0\x70\x0b\x60\x42\xc4\x5a\x1a\x6a\xa3\x85\x1d'
            b'\xf1\x31\x04\xdc\xa0\x70\xb3\x0a\xa3\xf5\x0a\xf1\x9d\x2e\x0d'
            b'\x25\x00\x60\x7d\x02\x17\x5f\x4b\x49\x94\x07\xb1\xc5\x47\x5f'
            b'\x03\xcc\xa1\xfc\x61\xfd\xd1\x48\x28\xf4\x79\x80\x1c\x39\xf0'
            b'\x67\x96\x40\x78\x42\x21\x10\x81\x74\xd7\x51\x04\xc0\xd1\x08'
            b'\xf4\x03\x9f\x13\xe5\x4b\x40\xae\x1e\x87\x7b\x66\x4a\x43\xde'
            b'\x42\xf7\x7d\x1b\x2e\x7c\x1f\x01\xc2\x6f\x04\xfa\xb0\x22\xd0'
            b'\x12\x77\xbb\xa6\x8b\xaa\xa0\x81\x90\x59\x14\x92\x59\x3c\xf3'
            b'\x81\x7f\x38\x87\x0b\x81\x08\x24\xb2\x5a\xeb\x7d\x6a\xc7\xdc'
            b'\x38\x00\x7c\x16\xe5\x6b\x08\x85\x46\x9b\xf9\x2b\x34\x94\x0f'
            b'\xe0\x70\xd6\x6e\x04\x04\x5f\x94\xf7\x61\x93\x8a\x2c\x8b\xbb'
            b'\x4d\xd3\x45\xb5\x76\x59\xc4\x6a\xf9\xde\x8e\xaa\xb0\x1b\xf8'
            b'\xb4\xd8\x4c\x58\xa5\x1b\x1b\xc4\xe1\x37\x11\x0d\x7f\x1b\xad'
            b'\xdd\x68\xfd\x59\x1e\xbc\x1d\x1b\x2c\xb4\x3a\xee\x36\x39\x1c'
            b'\x53\xf0\x3c\x70\x7d\x00\x3f\xf4\x20\xaa\x45\x26\xdf\x6a\xd2'
            b'\xf0\x46\xe4\x4d\x57\x82\x6f\x6b\x37\x7e\x1f\xf8\x10\xd6\x41'
            b'\xe8\x70\x34\x22\x0f\x02\x7f\x98\x29\xf0\x1f\x09\x6d\xfc\xc1'
            b'\x0f\x4d\x20\x00\x60\x73\x0b\x16\x80\x52\x92\x9f\x63\x45\xe0'
            b'\x76\x9c\x6f\xdb\xd1\x38\x28\xf6\x9e\xfc\x60\x29\xc1\xcf\xf3'
            b'\xc9\xf8\x62\xfb\x67\x4a\x43\x3a\x01\x27\xe2\xbe\xef\xc0\xc5'
            b'\xef\x06\x03\x7b\x15\xee\x15\x7b\x6e\xe0\x54\x1a\xa8\x08\xa9'
            b'\x63\x41\x52\x04\xbe\x8d\xf2\x09\x51\x5e\x40\xac\xd5\xda\x2c'
            b'\x34\xbc\x0f\x60\x22\xca\x49\x45\x3a\x80\x8f\x03\x9f\x00\xba'
            b'\xe3\x6e\x93\x63\x41\xd2\x07\x7c\xa9\xfc\xe8\x6f\x94\xe8\xbe'
            b'\x99\xd0\x94\x02\x00\x56\x04\x14\x92\x02\xef\x00\xfe\x0a\x58'
            b'\x13\x77\x9b\x1c\x0b\x8a\x67\x81\xbf\x54\xf8\x3e\x50\x6c\xa6'
            b'\x59\x7f\x3c\x4d\xe1\x03\x98\x88\x0d\x57\x42\x28\x14\xf7\x64'
            b'\xf8\x1e\xf0\x5e\xe0\x4e\xc0\x1d\x78\x77\xd4\x1a\x05\x7e\x0a'
            b'\xbc\xbf\xa3\x8f\xef\x7a\x51\xf3\x0e\x7e\x68\x62\x0b\xa0\xc2'
            b'\xba\x5b\x41\x7c\xd0\x90\x95\x08\x9f\x04\x7e\x1f\x68\x8d\xbb'
            b'\x5d\x8e\x79\xc9\x30\xf0\x2d\x94\x2f\x9a\x88\x6d\x41\x4c\x59'
            b'\x7c\xaa\x49\xd3\x0b\x40\x85\xb2\x5f\x20\x0b\xfc\x0e\x70\x3d'
            b'\x6e\x49\xe0\xa8\x2e\xcf\x63\xe3\x50\xbe\x0b\x8c\x34\xe3\x7a'
            b'\x7f\x22\xe6\x8d\x00\x00\x5c\x77\x07\xe4\xb2\x48\x76\x90\x57'
            b'\x61\x6b\x0f\x5c\x45\x13\x1e\x26\x72\x34\x14\x45\x60\x13\xca'
            b'\xdf\x98\x02\x0f\x47\x49\x74\xc3\xd5\x71\x37\xa9\x7a\xcc\x2b'
            b'\x01\x00\xf8\xaf\xdf\x83\x74\x3b\x68\x48\x37\x86\x0f\x03\x7f'
            b'\x4a\x0c\xf9\x06\x1d\xf3\x82\xdd\xc0\x57\x54\xf8\x07\x0f\x0e'
            b'\x0c\x28\x7c\x6d\x9e\xcc\xfc\x15\xe6\x9d\x00\x54\x58\xb7\x09'
            b'\x10\x7c\x22\xde\x00\x7c\x12\x78\x2d\xf5\xac\x46\xe4\x68\x66'
            b'\x4a\xc0\xcf\x80\x2f\xa2\xfc\x4c\x20\x68\x96\xc0\x9e\x99\x32'
            b'\x6f\x05\x00\x60\xdd\xed\x10\x05\x20\x1e\x3d\xa2\x7c\x18\xf8'
            b'\x08\xb0\x22\xee\x76\x39\x1a\x9a\x6d\xc0\xd7\x54\xf8\x46\x51'
            b'\xd8\x93\x89\xe0\x86\x79\x36\xeb\x8f\x67\x5e\x0b\x40\x85\xf5'
            b'\x9b\x00\xf0\x55\xb9\x00\xb8\x0e\xb8\x9c\x26\xcb\x31\xe0\xa8'
            b'\x39\x39\xe0\x0e\xe0\x46\xe0\x7e\x84\x68\x43\x7d\xeb\x56\xc5'
            b'\xc2\x82\x10\x00\x80\x75\x3f\xc5\x7e\xc5\x1e\x9d\x44\xbc\x1b'
            b'\xf8\x18\x70\xc6\x42\xea\x03\xc7\x84\x44\xc0\x53\xc0\x57\x54'
            b'\xf9\xae\xe7\xd3\x3f\x3a\x02\x7f\xff\xce\xb8\x9b\x55\x1f\x16'
            b'\xdc\xcd\xbf\x76\x13\x04\x3e\x92\x28\x71\x32\x76\x49\x70\x2d'
            b'\x4d\x94\x67\xc0\x51\x55\x76\x00\xdf\x06\xbe\x0e\xbc\x00\xe8'
            b'\x7c\xd9\xde\x9b\x2e\x0b\x4e\x00\x2a\xac\xbf\x0d\x50\x92\x6a'
            b'\xb8\x10\xf8\x63\xec\x96\x61\x5b\xdc\xed\x72\xd4\x85\x21\xe0'
            b'\x56\xe0\xef\x45\x78\x48\xa1\xb4\x10\xcc\xfd\x89\x58\xb0\x02'
            b'\x00\xf0\x8e\xfd\x70\xca\xaf\x20\xf4\xc9\xa2\x5c\x2e\xf0\x27'
            b'\xd8\xba\x04\x99\xb8\xdb\xe6\xa8\x09\x79\xe0\x3e\xe0\xab\x6a'
            b'\xd7\xfb\x23\xcd\x1c\xc6\x5b\x0d\x16\xb4\x00\x54\xb8\xfe\x56'
            b'\xf0\xf3\x50\xca\xb0\x48\x85\xab\x81\x3f\x02\xce\xc3\x05\x11'
            b'\xcd\x17\x8a\xc0\x23\xc0\xd7\x05\x7e\x30\x08\xfb\xdb\xb0\xe7'
            b'\x49\x16\x3a\x4e\x00\xc6\xb1\x7e\x23\x78\x02\xa1\xb2\x4c\xe1'
            b'\x1a\xe0\x03\x38\x21\x68\x66\x0a\xd8\x62\x33\xdf\x04\x7e\x10'
            b'\xc2\x6e\x03\xba\xd0\x67\xfd\xf1\x38\x01\x98\x80\xf5\x1b\x6d'
            b'\x59\xa2\x3c\xf4\x88\xf5\x0d\xbc\x1b\xb8\x90\x26\x2d\x54\xb2'
            b'\x00\xc9\x03\x0f\x03\xff\x1b\xb8\x25\x54\xf6\x18\x71\x03\x7f'
            b'\x22\x9c\x00\x4c\xc1\xba\x8d\xb6\xa8\x87\x86\x74\x21\x5c\x8a'
            b'\xdd\x31\x78\x03\x2e\x01\x49\xa3\x32\x00\xdc\xab\xf0\x3d\x51'
            b'\x7e\xec\x47\xec\x0b\x0d\x3a\x5f\xa3\xf8\xaa\x81\x13\x80\x69'
            b'\xf0\xa9\x3b\xa0\x7f\x04\x5a\xd3\x64\x51\x5e\xad\xc2\x7b\x80'
            b'\x2b\x80\xe5\x34\x51\x5a\xb5\x79\x4a\x04\xec\xc2\x3a\xf5\xfe'
            b'\x4d\x85\x5f\xee\x0d\x18\x5c\xe2\xc1\xcd\x6e\xc6\x3f\x2a\x4e'
            b'\x00\x66\xc8\xfa\xdb\x00\x48\xaa\x70\x2a\x76\x79\xf0\x76\xe0'
            b'\x4c\x9a\xa8\x70\xc9\x3c\x61\x14\x1b\xc0\x73\x2b\xf0\x23\x89'
            b'\x78\x52\x1b\xb8\x00\x47\xa3\xe2\x04\x60\x96\xac\xdd\x04\x22'
            b'\x08\x11\x4b\xb1\x07\x8d\xae\x00\x2e\x03\x56\xe2\x12\x95\xd6'
            b'\x8a\x00\xd8\x09\xdc\x03\xdc\x22\x70\x9f\x89\xd8\x13\x89\x33'
            b'\xf3\x67\x8b\x13\x80\x2a\xb0\xfe\x56\x00\x92\x18\x56\xab\x15'
            b'\x81\x37\x63\xcb\x99\x2d\xa1\x89\xd3\xae\x35\x08\x21\xb6\xcc'
            b'\xd6\xc3\xc0\x26\xe0\x27\xaa\x6c\x16\xdc\x6c\x5f\x0d\x9c\x00'
            b'\x54\x91\xeb\x36\x42\x31\x82\xb4\x21\x8b\x70\x1a\xca\xa5\x58'
            b'\xa7\xe1\xb9\xd8\x34\xe6\xce\x32\x98\x1e\x01\xd0\x0b\x3c\x06'
            b'\xdc\xa9\xf0\x53\x51\x9e\x45\x18\x02\xb7\x7f\x5f\x4d\x9c\x00'
            b'\xd4\x88\x75\x1b\x6d\xfd\x3e\x55\xda\x50\x4e\x46\xb8\x18\xbb'
            b'\x95\x78\x3e\xf6\x48\xb2\x8b\x36\x3c\x94\x1c\x36\x01\xc7\x6f'
            b'\x80\x9f\x23\xfc\x02\xe5\x05\x42\x86\x90\xf9\x95\x85\xa7\x91'
            b'\x70\x02\x50\x07\x3e\x75\x07\x9c\xd6\x0d\x8f\xed\x23\xad\xc2'
            b'\x0a\x51\xce\xc5\x0a\xc1\xf9\xc0\x29\x40\x27\x0b\xef\x78\x72'
            b'\x11\x9b\x57\xff\x59\xe0\x01\x94\xfb\x55\x78\x44\x60\x57\x00'
            b'\xa3\x06\xe7\xc5\xaf\x07\x4e\x00\x62\xe0\xba\xdb\x01\x30\x46'
            b'\x69\x07\x56\xa2\x9c\x85\x8d\x38\x7c\x25\x70\x32\x36\xce\xa0'
            b'\x85\xf9\xf3\xfd\x28\x30\x82\x1d\xf0\xcf\x03\x8f\x0a\x3c\xa6'
            b'\x36\x4a\x6f\x8b\xc0\x20\x10\x35\x72\x15\xdd\xf9\xca\x7c\xb9'
            b'\xc1\x9a\x9a\xf5\x36\xa3\xb1\x07\xb4\xaa\xb2\x14\xbb\xc5\x78'
            b'\x1a\x56\x0c\xd6\x00\xc7\x63\x4f\x2a\xb6\x60\x83\x14\x1b\x99'
            b'\x00\xbb\x45\x37\x08\x6c\x07\x9e\xc3\x6e\xd7\x3d\x09\x3c\xa3'
            b'\xb0\x4f\x0c\xc3\x28\xe1\x42\x3d\x81\xd7\x48\x38\x01\x68\x40'
            b'\x3e\xff\x2b\x78\x79\x0b\xb4\x77\xe0\x47\xd0\x86\xd0\x89\x72'
            b'\x2c\x70\x22\x70\x02\xb0\x0a\x38\xa6\xfc\xe8\xc4\x2e\x1f\x52'
            b'\xe5\x47\xad\x1d\x8d\x01\x36\xc6\xbe\x80\x0d\xb9\xed\xc7\x9e'
            b'\xab\xdf\x5e\xfe\xfb\x65\xe0\x25\xe0\x25\x84\x5e\x51\x86\x3b'
            b'\x52\x14\x47\x02\xf8\xfc\x5b\xe3\xee\x59\xc7\xe1\x38\x01\x68'
            b'\x22\xae\xff\x21\x78\x21\x94\x92\x24\x31\x64\x81\x16\x81\x6e'
            b'\xb5\x4e\xc5\xe5\xd8\xc4\x26\x8b\x80\xc5\xd8\x65\x44\x07\xd0'
            b'\x8e\x2d\x94\xd2\x82\x15\x8a\x34\x56\x24\x3c\x0e\x26\x49\x2d'
            b'\x61\xb7\xdb\x02\xec\xa0\xce\x63\x67\xf1\x61\x6c\x78\xed\x20'
            b'\xd6\x2b\xbf\x1f\xbb\x25\xb7\x07\xd8\x85\xb2\x13\xa1\x57\x95'
            b'\x51\x60\x24\x4c\x52\x34\x61\xf3\x17\xcb\x58\x48\xfc\x5f\x1a'
            b'\x25\xbd\xc5\xa6\xe7\x47\x83\x00\x00\x00\x25\x74\x45\x58\x74'
            b'\x64\x61\x74\x65\x3a\x63\x72\x65\x61\x74\x65\x00\x32\x30\x31'
            b'\x37\x2d\x30\x38\x2d\x30\x32\x54\x31\x32\x3a\x35\x38\x3a\x32'
            b'\x30\x2b\x30\x32\x3a\x30\x30\xe6\x5e\x2e\x14\x00\x00\x00\x25'
            b'\x74\x45\x58\x74\x64\x61\x74\x65\x3a\x6d\x6f\x64\x69\x66\x79'
            b'\x00\x32\x30\x31\x37\x2d\x30\x38\x2d\x30\x32\x54\x31\x32\x3a'
            b'\x35\x38\x3a\x32\x30\x2b\x30\x32\x3a\x30\x30\x97\x03\x96\xa8'
            b'\x00\x00\x00\x46\x74\x45\x58\x74\x73\x6f\x66\x74\x77\x61\x72'
            b'\x65\x00\x49\x6d\x61\x67\x65\x4d\x61\x67\x69\x63\x6b\x20\x36'
            b'\x2e\x37\x2e\x38\x2d\x39\x20\x32\x30\x31\x36\x2d\x30\x36\x2d'
            b'\x31\x36\x20\x51\x31\x36\x20\x68\x74\x74\x70\x3a\x2f\x2f\x77'
            b'\x77\x77\x2e\x69\x6d\x61\x67\x65\x6d\x61\x67\x69\x63\x6b\x2e'
            b'\x6f\x72\x67\xe6\xbf\x34\xb6\x00\x00\x00\x18\x74\x45\x58\x74'
            b'\x54\x68\x75\x6d\x62\x3a\x3a\x44\x6f\x63\x75\x6d\x65\x6e\x74'
            b'\x3a\x3a\x50\x61\x67\x65\x73\x00\x31\xa7\xff\xbb\x2f\x00\x00'
            b'\x00\x18\x74\x45\x58\x74\x54\x68\x75\x6d\x62\x3a\x3a\x49\x6d'
            b'\x61\x67\x65\x3a\x3a\x68\x65\x69\x67\x68\x74\x00\x35\x31\x32'
            b'\xc0\xd0\x50\x51\x00\x00\x00\x17\x74\x45\x58\x74\x54\x68\x75'
            b'\x6d\x62\x3a\x3a\x49\x6d\x61\x67\x65\x3a\x3a\x57\x69\x64\x74'
            b'\x68\x00\x35\x31\x32\x1c\x7c\x03\xdc\x00\x00\x00\x19\x74\x45'
            b'\x58\x74\x54\x68\x75\x6d\x62\x3a\x3a\x4d\x69\x6d\x65\x74\x79'
            b'\x70\x65\x00\x69\x6d\x61\x67\x65\x2f\x70\x6e\x67\x3f\xb2\x56'
            b'\x4e\x00\x00\x00\x17\x74\x45\x58\x74\x54\x68\x75\x6d\x62\x3a'
            b'\x3a\x4d\x54\x69\x6d\x65\x00\x31\x35\x30\x31\x36\x37\x31\x35'
            b'\x30\x30\x47\xfb\xd2\x91\x00\x00\x00\x11\x74\x45\x58\x74\x54'
            b'\x68\x75\x6d\x62\x3a\x3a\x53\x69\x7a\x65\x00\x32\x32\x4b\x42'
            b'\x42\x36\xc0\xe2\x5e\x00\x00\x00\x43\x74\x45\x58\x74\x54\x68'
            b'\x75\x6d\x62\x3a\x3a\x55\x52\x49\x00\x66\x69\x6c\x65\x3a\x2f'
            b'\x2f\x2e\x2f\x75\x70\x6c\x6f\x61\x64\x73\x2f\x63\x61\x72\x6c'
            b'\x6f\x73\x70\x72\x65\x76\x69\x2f\x61\x4e\x6d\x4d\x41\x30\x48'
            b'\x2f\x31\x33\x31\x30\x2f\x62\x6f\x6f\x6b\x5f\x38\x36\x33\x34'
            b'\x35\x2e\x70\x6e\x67\x36\x92\x3f\x08\x00\x00\x00\x00\x49\x45'
            b'\x4e\x44\xae\x42\x60\x82'))
        img = ImageTk.PhotoImage(img)
        Label(
            self,
            image=img,
            background='#DF9953'
        ).place(anchor='c', rely=.35, relx=.5)
        Label(
            self,
            text='F_Reference_H',
            font=('Time New Roman', 25, 'bold italic'),
            background='#DF9953',
        ).place(relx=.5, rely=.6, anchor='c')
        Label(
            self,
            text='Используя программу, Вы даёте разрешение на обработку '
                 'ваших персональных данных и \nВы соглашаетесь с условиями '
            'лицензионного соглашения',
            font=('Times New Roman', 9, 'italic'),
            background='#DF9953',
            foreground='#242424',
            justify='center'
        ).place(relx=.5, rely=.93, anchor='c')
        Label(
            self,
            font=('Times New Roman', 9, 'italic'),
            text=f'Подробнее на сайте: {SAIT}',
            background='#DF9953',
            foreground='#242424',
            justify='center'
        ).place(relx=.5, rely=.97, anchor='c')
        Label(
            self,
            font=('Times New Roman', 10, 'italic bold'),
            text='Version: ' + VERSION,
            justify='center',
            background='#DF9953',
            foreground='#242424'
        ).place(relx=.5, rely=.02, anchor='c')
        self.update()


class Build(Chek_value, Actions):
    def __init__(self):
        self.Main_window = ThemedTk(theme='black')
        self.Main_window.withdraw()
        self.Main_window.title('F_Reference_H')
        self.Main_window.geometry('1200x500')
        x = (self.Main_window.winfo_screenwidth() -
             self.Main_window.winfo_reqwidth()) / 4
        y = (self.Main_window.winfo_screenheight() -
             self.Main_window.winfo_reqheight()) / 4
        self.Main_window.wm_geometry("+%d+%d" % (x - 70, y + 50))
        self.Main_window.resizable(width=False, height=False)
        super().__init__()
        self.download_page()
        splash = Splash()
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
            ).place(y=34, x=1)
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
                lambda no_matter: webopen(VK)
            )
            self.optimaze_flowhack_1.place(x=5, rely=.265)
            self.optimaze_flowhack_2 = Label(
                self.optimization_block,
                image=self.average_flowhack,
                cursor='heart'
            )
            self.optimaze_flowhack_2.bind(
                '<Button-1>',
                lambda no_matter: webopen(VK)
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
                var=self.chk_pas_upper,
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
            Button(
                self.pas_generator_block,
                text=LANGUAGE[self.language]['pas_generator_reset'],
                cursor='exchange',
                command=self.password_generator_reset
            ).place(rely=.5, anchor='c', relx=.5)
            Label(
                self.pas_generator_block,
                text=LANGUAGE[self.language]['pas_generator_result'],
                font=('Times New Roman', 12, 'bold italic')
            ).place(anchor='c', relx=.5, rely=.61)
            self.pas_generator_result = Entry(
                self.pas_generator_block,
                state=DISABLED,
                font=('Times New Roman', 12, 'bold'),
                justify='center',
                foreground='black'
            )
            self.pas_generator_result.place(
                anchor='c',
                relx=.5,
                rely=.68,
                relwidth=.9,
                height=25
            )
            Button(
                self.pas_generator_block,
                text=LANGUAGE[self.language]['pas_generator_create'],
                command=self.password_generate,
                cursor='hand1'
            ).place(anchor='c', relx=.5, rely=.77)
            flowhack_pas_generate_1 = Label(
                self.pas_generator_block,
                image=self.max_flowhack
            )
            flowhack_pas_generate_1.bind(
                '<Button-1>',
                lambda no_matter: webopen(VK)
            )
            flowhack_pas_generate_1.place(relx=.05, rely=.92)
            flowhack_pas_generate_2 = Label(
                self.pas_generator_block,
                image=self.max_flowhack
            )
            flowhack_pas_generate_2.bind(
                '<Button-1>',
                lambda no_matter: webopen(VK)
            )
            flowhack_pas_generate_2.place(relx=.81, rely=.92)

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
            state='readonly',
            cursor='hand2'
        )
        self.input_language.set(self.language)
        self.input_language['values'] = LANGUAGE_LIST
        self.input_language.place(relx=.6, y=50, anchor='c')
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
            lambda no_matter: webopen(VK)
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
            lambda no_matter: webopen(VK)
        )
        self.lbl_set_flowhack_1.place(relx=.05, rely=.92)
        self.lbl_set_flowhack_2 = Label(
            self.settings_block,
            image=self.max_flowhack,
            cursor='heart'
        )
        self.lbl_set_flowhack_2.bind(
            '<Button-1>',
            lambda no_matter: webopen(VK)
        )
        self.lbl_set_flowhack_2.place(relx=.81, rely=.92)

        # !!!!!! BUILD_HELP_BLOCK !!!!!!
        Label(
            self.help_block,
            font=('Times New Roman', 14, 'bold italic'),
            text=LANGUAGE[self.language]['HELP_TEXT'],
            justify='center'
        ).place(relx=.5, rely=.4, anchor='c')
        Label(
            self.help_block,
            font=('Times New Roman', 11, 'bold italic'),
            text='Version: ' + VERSION
        ).place(relx=.5, rely=.97, anchor='c')
        self.btn_help_copy = Button(
            self.help_block,
            text=LANGUAGE[self.language]['HELP_SAIT'],
            cursor='heart',
            command=self.copy_help,
        )
        self.btn_help_copy.place(anchor='c', relx=.5, rely=.5)
        flowhack_help_1 = Label(
            self.help_block,
            image=self.max_flowhack,
            cursor='heart'
        )
        flowhack_help_1.bind(
            '<Button-1>',
            lambda no_matter: webopen(VK)
        )
        flowhack_help_1.place(relx=.05, rely=.92)
        flowhack_help_2 = Label(
            self.help_block,
            image=self.max_flowhack,
            cursor='heart',
            justify='center'
        )
        flowhack_help_2.bind(
            '<Button-1>',
            lambda no_matter: webopen(VK)
        )
        flowhack_help_2.place(relx=.81, rely=.92)
        Label(
            self.help_block,
            text=LANGUAGE[self.language]['help_license'],
            font=('Times New Roman', 10, 'italic'),
            justify='center'
        ).place(relx=.5, rely=.9, anchor='c')

        sleep(2)
        splash.destroy()
        self.Main_window.deiconify()
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
        def chek_save():
            if doing == 'EDIT':
                text, text_old = \
                    self.text_addedit.get(1.0, END), addedit_all[2] + '\n'
                name, name_old = \
                    self.input_addedit_name.get().lstrip().rstrip(), \
                    addedit_all[1]
                if (text == text_old) and (name == name_old):
                    self.Add_edit_window.destroy()
                else:
                    answer = askyesnocancel(
                        'Exit?',
                        LANGUAGE[self.language]['add_edit_exit_or_no']
                    )
                    if answer:
                        save()
                    elif answer == bool(False):
                        self.Add_edit_window.destroy()
                    else:
                        pass
            else:
                text = self.text_addedit.get(1.0, END)
                name = self.input_addedit_name.get().lstrip().rstrip()
                if (text.isspace() == bool(False)) or \
                        ((name != '') and (name != ' ')):
                    answer = askyesnocancel('Exit?', LANGUAGE[self.language][
                        'add_edit_exit_or_no'])
                    if answer:
                        save()
                    elif answer == bool(False):
                        self.Add_edit_window.destroy()
                    else:
                        pass
                else:
                    self.Add_edit_window.destroy()

        def apply():
            return self.text_addedit.configure(
                font=(
                    self.input_addedit_font.get(),
                    self.input_size_addedit.get()
                )
            )

        def save():
            name = self.input_addedit_name.get().lstrip().rstrip()
            font = self.input_addedit_font.get()
            size = self.input_size_addedit.get()
            text = self.text_addedit.get(1.0, END)
            try:
                if len(name) > 40:
                    raise NameError('Record too long')
                if not set(":;!*#¤&").isdisjoint(name):
                    raise NameError('unacceptable_symbols')
                if name == 'name':
                    raise NameError('name')
                if text == 'text':
                    raise NameError('text')
                if (text == '') or (text == ' '):
                    raise NameError('text_null')
                if name == '':
                    raise NameError('name_null')

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
                if str(error) == 'name':
                    showerror(
                        'Error',
                        ERROR[self.language]['not_name']
                    )
                if str(error) == 'text':
                    showerror(
                        'Error',
                        ERROR[self.language]['not_text']
                    )
                if str(error) == 'text_null':
                    showerror(
                        'Error',
                        ERROR[self.language]['text_null']
                    )
                if str(error) == 'name_null':
                    showerror(
                        'Error',
                        ERROR[self.language]['name_null']
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
        self.Add_edit_window.protocol("WM_DELETE_WINDOW", chek_save)

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
            lambda no_matter: webopen(VK)
        )
        label_flowhack_1.place(relx=.1, anchor='c', y=20)
        label_flowhack_2 = Label(
            self.Add_edit_window,
            image=self.average_flowhack,
            cursor='heart'
        )
        label_flowhack_2.bind(
            '<Button-1>',
            lambda no_matter: webopen(VK)
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
