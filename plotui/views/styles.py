import tkinter as tk


class BlueButton(tk.Button):
    """
    A pretty custom blue button.
    """
    def __init__(self, master, text, command):
        super().__init__(
            master=master, text=text, command=command, font="Helvetica 8 bold",
            bg='#1874CD', fg='white', activebackground='#104E8B', bd=2,
            highlightthickness=0,
            )
