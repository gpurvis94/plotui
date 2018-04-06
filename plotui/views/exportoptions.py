import tkinter as tk
from tkinter import ttk

from views.styles import BlueButton


class ExportOptionsFrame(ttk.Frame):
    """
    The visual design for the Plot element.
    """
    def __init__(self, parent, controller):
        # Initialize frame
        ttk.Frame.__init__(self, parent, style='Sub.TFrame', border=5)
        self.c = controller

        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self):
        # Instantiate nested widgets
        self.main_title_lbl = ttk.Label(self, text="Export Options",
                                style='Title.TLabel')

    def _position_widgets(self):
        # Position nested widgets
        self.main_title_lbl.grid(row=0, column=0, columnspan=1)

        # Configure rows and columns
        self.grid_columnconfigure(0, pad=5)

