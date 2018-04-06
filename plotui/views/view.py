import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from views.mainwindow import MainWindowFrame


class View(tk.Tk):
    """
    The root level element.
    """
    def __init__(self):
        # Initialise the base level element
        super().__init__()

        # Create styles
        self._create_styles()

        # Instantiate and grid the main frame
        self.main_frame = MainWindowFrame(self)
        self.main_frame.grid()

        # Enter the event loop
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
        self.s.configure('TFrame', background='white')
        self.s.configure('Sub.TFrame', background='white', relief=tk.GROOVE,
                         borderwidth=1)
        self.s.configure('Main.TFrame', background='white', relief=tk.SUNKEN)

        # Labels
        self.s.configure('TLabel', background='white')
        self.s.configure('SubTitle.TLabel', font=self.sub_title_font,
                         padding="2")
        self.s.configure('Title.TLabel', font=self.title_font, padding="4")
        self.s.configure('TButton', background='white')

        # Checkbuttons
        self.s.configure('TCheckbutton', background='white')