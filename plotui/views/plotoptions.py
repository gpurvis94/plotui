from tkinter import ttk

from views.styles import BlueButton


class PlotOptionsFrame(ttk.Frame):
    """
    The visual design for the Plot element.
    """
    def __init__(self, parent, controller):
        # Initialize frame
        ttk.Frame.__init__(self, parent, style='Sub.TFrame', border=5)
        self.controller = controller

        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self):
        # Instantiate nested widgets
        self.title_lbl = ttk.Label(self, text="Plot Options",
                                   style='Title.TLabel')
        self.button1 = BlueButton(master=self, text="Add Plot",
                                  command=self.plot_model_line,)
        self.button2 = BlueButton(master=self, text="Remove Plot",
                                  command=self.remove_line,)

    def _position_widgets(self):
        # Position nested widgets
        self.title_lbl.grid(row=0, column=0)
        self.button1.grid(row=1, column=0)
        self.button2.grid(row=2, column=0)

        # Configure rows and columns
        self.grid_columnconfigure(0, weight=1)

    def plot_model_line(self):
        self.controller.plot_model_line()

    def remove_line(self):
        self.controller.remove_line()
