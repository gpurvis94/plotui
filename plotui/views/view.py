import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from views.mainwindow import MainWindowFrame


class View(tk.Tk):
    """
    The root level element.
    """
    def __init__(self):
        super().__init__()

        self._create_styles()

        self.main_frame = MainWindowFrame(self)
        self.main_frame.grid()

        self.mainloop()

    def _create_styles(self):
        self.s = ttk.Style()

        # Fonts
        self.standard_font = Font(family="Helvetica", size=8)
        self.sub_title_font = Font(family="Helvetica", size=10, underline=1)
        self.title_font = Font(family="Helvetica", size=12, underline=1,
            weight='bold')

        # Set universal widget properties
        self.s.configure('.', font=self.standard_font, foreground='black')

        # Frames
        self.s.configure('Main.TFrame', background='white', relief=tk.SUNKEN)
        self.s.configure('Sub.TFrame', background='white', relief=tk.GROOVE,
            borderwidth=1)
        self.s.configure('TFrame', background='white')

        # Labels
        self.s.configure('Title.TLabel', font=self.title_font)
        self.s.configure('SubTitle.TLabel', font=self.sub_title_font)
        self.s.configure('TLabel', background='white')

        # Entrys
        self.s.configure('Number.TEntry')
        self.s.configure('String.TEntry')

        # Checkbuttons
        self.s.configure('TCheckbutton', background='white')

        # Comboboxes
        self.s.configure('TCombobox')

        # Radiobuttons
        self.s.configure('TRadiobutton', background='white')
        