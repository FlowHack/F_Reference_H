from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from sys import exit as exit_ex
from tkinter.ttk import Checkbutton, Frame, Label
from tkinter import BooleanVar, PhotoImage, DISABLED


class App(ThemedTk):
    def __init__(self):
        ThemedTk.__init__(self, theme='black')
        self.title('Installer')
        self.geometry('500x200')
        x = (self.winfo_screenwidth() -
             self.winfo_reqwidth()) / 4
        y = (self.winfo_screenheight() -
             self.winfo_reqheight()) / 4
        self.wm_geometry("+%d+%d" % (x - 70, y + 50))
        self.resizable(width=False, height=False)
        self.iconphoto(True, PhotoImage(
            file='bin/ico/ico_main.png'))
        flow_hack_png = Image.open(f'bin/ico/max_flowhack.png')
        flow_hack_png = ImageTk.PhotoImage(flow_hack_png)
        Frame(self).place(relwidth=1, relheight=1)

        flow_hack_label = Label(
            self,
            image=flow_hack_png
        ).place(anchor='c', relx=.5, rely=.1)
        self.check_icon = BooleanVar()
        self.check_icon.set(bool(True))
        Checkbutton(
            self,
            text='Create a shortcut on the desktop',
            var=self.check_icon,
            cursor='cross'
        ).place(relx=.5, y=60, anchor='c')
        Label(
            self,
            text='Select a folder to install',
            font=('Times New Roman', 11, 'bold italic')
        ).place(x=10, rely=.45)

        self.mainloop()


if __name__ == '__main__':
    build = App()