from os import name, getcwd
from tkinter import PhotoImage
from tkinter.messagebox import showerror
from tkinter.ttk import Label, Button, Frame
from webbrowser import open as webopen
import requests
import sys
from subprocess import Popen

from ttkthemes import ThemedTk
from PIL import Image, ImageTk

URL_FILE = 'https://flowhack.github.io/download/Windows/distro/bin/dist/F_Reference_H/F_Reference_H.exe'
NAME_FILE = 'F_Reference_H.exe'
SAIT = 'https://flowhack.github.io/'
VK = 'http://vk.com/id311966436'
PATH = getcwd()


def open_app():
    if name == 'nt':
        Popen(f'{PATH}/F_Reference_H.exe')

    sys.exit()


class Update(ThemedTk):
    def __init__(self):
        ThemedTk.__init__(self, theme='black')
        self.title('Обновление F_Reference_H')
        self.geometry('500x140')
        x = (self.winfo_screenwidth() -
             self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() -
             self.winfo_reqheight()) / 2
        self.wm_geometry("+%d+%d" % (x - 150, y))
        self.resizable(width=False, height=False)
        self.iconphoto(
            True,
            PhotoImage(file='settings/ico/ico_main.png')
        )
        flow_hack_png = Image.open(f'settings/ico/mini_flowhack.png')
        flow_hack_png = ImageTk.PhotoImage(flow_hack_png)
        self.frame = Frame(self)
        self.frame.place(relwidth=1, relheight=1)

        flow_1 = Label(
            self.frame,
            image=flow_hack_png,
            cursor='heart'
        )
        flow_1.bind(
            '<Button-1>',
            lambda no_matter: webopen(VK)
        )
        flow_1.place(relx=.09, rely=.085, anchor='center')
        flow_2 = Label(
            self.frame,
            image=flow_hack_png,
            cursor='heart'
        )
        flow_2.bind(
            '<Button-1>',
            lambda no_matter: webopen(VK)
        )
        flow_2.place(relx=.91, rely=.085, anchor='center')
        self.lbl_done = Label(
            self.frame,
            text='ОБНОВЛЕНИЕ',
            font=('Times New Roman', 12, 'bold italic')
        )
        self.lbl_done.place(relx=.5, rely=.1, anchor='c')
        self.lable_second = Label(
            self.frame,
            text='Нам понадобится интернет!\nМы всё сделаем сами, это не '
                 'займё много времени!',
            font=('Times New Roman', 10, 'bold italic'),
            justify='center'
        )
        self.lable_second.place(relx=.5, rely=.35, anchor='c')
        self.btn_update = Button(
            self.frame,
            text='Обновить',
            cursor='hand1',
            command=self.updater_window
        )
        self.btn_update.place(relx=.5, rely=.65, anchor='c')
        self.license = Label(
            self.frame,
            cursor='hand1',
            text='Нажимая "Обновить" вы принимаете лицензионное соглашение',
            font=('Times New Roman', 10, 'bold italic'),
            foreground='black'
        )
        self.license.bind('<Button-1>', lambda no_matter: webopen(SAIT))
        self.license.place(relx=.5, rely=.92, anchor='c')

        self.mainloop()

    def updater_window(self):
        try:
            if name == 'nt':
                with open(NAME_FILE, "wb") as f:
                    response = requests.get(URL_FILE, stream=True)
                    total_length = int(response.headers.get('content-length'))
                    self.btn_update.configure(
                        text=f'Размер: {total_length / 1024 / 1024:0.2f} Mb'
                    )
                    self.btn_update.update()

                    if total_length is None:
                        f.write(response.content)
                    else:
                        dl = 0
                        for data in response.iter_content(chunk_size=4096):
                            dl += len(data)
                            f.write(data)
                            done = int(50 * dl / total_length)
                            self.license.configure(
                                text=f'\r{"=" * done}{" " * (50 - done)}'
                            )
                            self.license.update()
                            sys.stdout.flush()
                        self.lbl_done.configure(
                            text='Готово!',
                            foreground='#DA9958'
                        )
                        self.btn_update.configure(
                            text='Открыть программу',
                            command=open_app
                        )
            elif name == 'posix':
                showerror(
                    'Error',
                    'К сожалению на Linux пока нельзя обновиться'
                )
                self.btn_update.configure(
                    text='Закрыть',
                    command=open_app
                )
        except requests.exceptions.ConnectionError:
            showerror(
                'Error',
                'Произошла ошибка!\n\nПохоже, что у вас отсутствует '
                'подключение к интернету!\n\nЕсли не получается решить '
                'проблему, то напишите мне в блоке "Обратная связь" '
            )


if __name__ == '__main__':
    updater = Update()
