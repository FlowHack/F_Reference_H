from os import getcwd, path, system
from shutil import move as move_file
from sys import exit as exit_ex
from tkinter import DISABLED, END, NORMAL, BooleanVar, PhotoImage
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo
from tkinter.ttk import Button, Checkbutton, Entry, Frame, Label
from webbrowser import open as webopen

from PIL import Image, ImageTk
from ttkthemes import ThemedTk


def open_web(no_matter=None):
    webopen('https://flowhack.github.io/')
    webopen('http://vk.com/id311966436')


class App(ThemedTk):
    def __init__(self):
        ThemedTk.__init__(self, theme='black')
        self.title('Установщик F_Reference_H')
        self.geometry('500x200')
        x = (self.winfo_screenwidth() -
             self.winfo_reqwidth()) / 2
        y = (self.winfo_screenheight() -
             self.winfo_reqheight()) / 2
        self.wm_geometry("+%d+%d" % (x - 150, y - 20))
        self.resizable(width=False, height=False)
        self.iconphoto(True, PhotoImage(
            file='bin/ico/ico_main.png'))
        flow_hack_png = Image.open(f'bin/ico/max_flowhack.png')
        flow_hack_png = ImageTk.PhotoImage(flow_hack_png)
        browse_png = Image.open(f'bin/ico/browse.png')
        browse_png = ImageTk.PhotoImage(browse_png)
        Frame(self).place(relwidth=1, relheight=1)
        self.url = ''
        self._path = getcwd()

        flow_hack_label = Label(
            self,
            image=flow_hack_png,
            cursor='heart'
        )
        flow_hack_label.bind('<Button-1>', open_web)
        flow_hack_label.place(anchor='c', relx=.5, rely=.1)
        self.check_icon = BooleanVar()
        self.check_icon.set(bool(True))
        Checkbutton(
            self,
            text='Создать ярлык на рабочем столе',
            var=self.check_icon,
            cursor='cross'
        ).place(relx=.5, y=60, anchor='c')
        Label(
            self,
            text='Выберите папку для установки',
            font=('Times New Roman', 10, 'bold italic')
        ).place(relx=.5, rely=.485, anchor='c')
        self.input_url = Entry(
            self,
            state=DISABLED,
            font=('Times New Roman', 9, 'bold italic'),
            foreground='black'
        )
        self.input_url.place(
            rely=.6,
            relx=.5,
            height=20,
            relwidth=.7,
            anchor='c'
        )
        Button(
            self,
            image=browse_png,
            cursor='hand1',
            command=self.directory
        ).place(relx=.86, rely=.455)
        Button(
            self,
            image=browse_png,
            cursor='hand1',
            command=self.directory
        ).place(relx=.045, rely=.455)
        Button(
            self,
            text='Установить',
            cursor='hand1',
            command=self.install
        ).place(relx=.5, rely=.75, anchor='c')
        self.license = Label(
            self,
            text='Для подтверждения согласия с лицензионным '
                 'соглашением\nНажмите на "Установить" правой кнопкой мыши',
            font=('Times New Roman', 9, 'bold italic'),
            foreground='black',
            cursor='hand1',
            justify='center'
        )
        self.license.bind(
            '<Button-1>',
            lambda no_matter: webopen('https://flowhack.github.io/')
        )
        self.license.place(relx=.5, rely=.93, anchor='c')

        self.mainloop()

    def directory(self):
        fits: bool = False
        while fits == bool(False):
            self.url = askdirectory()
            if ('\\' not in self.url) and ('/' not in self.url):
                showerror(
                    'Error',
                    'Мы заметили, что вы выбрали неверный адрес!'
                )
            else:
                fits: bool = True

        self.input_url.configure(state=NORMAL)
        self.input_url.insert(END, self.url)
        self.input_url.after(
            6000,
            lambda: self.input_url.configure(state=DISABLED)
        )

    def install(self):
        url = path.join(self.url)
        try:
            if url == '':
                raise NameError('is empty')
            elif ('\\' not in self.url) and ('/' not in self.url):
                raise NameError('not file')
            move_file('bin/dist/F_Reference_H', url)
            if self.check_icon.get():
                system(
                    f'@powershell \"$x=(New-Object -ComObject '
                    f'WScript.Shell).CreateShortcut('
                    f'\'%USERPROFILE%/Desktop/F_Reference_H.lnk\');$x'
                    f'.TargetPath=\''
                    f'{url}/F_Reference_H/F_Reference_H.py\';$x'
                    f'.WorkingDirectory=\''
                    f'{url}/F_Reference_H\';$x.Save()\" '
                )
                system(
                    f'@powershell \"$x=(New-Object -ComObject '
                    f'WScript.Shell).CreateShortcut('
                    f'\'%APPDATA%\Microsoft\Windows\Start '
                    f'Menu\Programs\F_Reference_H.lnk\');$x'
                    f'.TargetPath=\''
                    f'{url}/F_Reference_H/F_Reference_H.py\';$x'
                    f'.WorkingDirectory=\'{url}/F_Reference_H\';$x.Save()\"')
                showinfo('Successfully', 'Установка прошла успешно!')
                exit_ex()

        except NameError as error:
            if str(error) == 'is empty':
                showerror('Error', 'Пустое поле пути к папке!')
            if str(error) == 'not file':
                showerror(
                    'Error',
                    'Мы заметили, что вы выбрали неверный адрес!'
                )


if __name__ == '__main__':
    build = App()
