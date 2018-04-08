import tkinter as tk
from tkinter import ttk


class BaseFrame(ttk.Frame):
    """
    The base class for all custom frames. When initializing a custom
    frame, instead of using __init__(), override the methods below.
    """
    def __init__(self, parent, controller, style='TFrame', border=0):
        ttk.Frame.__init__(self, parent, style=style, border=border)
        self._c = controller

        self._init_variables()
        self._create_widgets()
        self._position_widgets()

    def _init_variables(self):
        pass

    def _create_widgets(self):
        pass

    def _position_widgets(self):
        pass


class SubFrame(BaseFrame):
    """
    A frame defining the properties of a frame within the main window.
    """
    def __init__(self, parent, controller, style='Sub.TFrame', border=5):
        super().__init__(parent, controller, style, border)


class SubSubFrame(BaseFrame):
    """
    A frame defining the properties of a frame within a SubFrame.
    """
    def __init__(self, parent, controller, style='TFrame', border=0):
        super().__init__(parent, controller, style, border)


class BlueButton(tk.Button):
    """
    A pretty custom blue button.
    """
    def __init__(self, master, text, command):
        super().__init__(
            master=master, text=text, command=command, font="Helvetica 8 bold",
            bg='#1874CD', fg='white', activebackground='#104E8B', bd=2,
            highlightthickness=0
            )
