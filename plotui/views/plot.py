from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PlotFrame(ttk.Frame):
    """
    The visual design for the Plot frame.
    """
    def __init__(self, parent, controller):
        # Initialize frame
        ttk.Frame.__init__(self, parent, style='Sub.TFrame', border=10)
        self.controller = controller

        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self):
        # Instantiate nested widgets
        self.canvas = FigureCanvasTkAgg(self.controller.get_plot_figure(),
                                        self,)
        self.plot = self.canvas.get_tk_widget()

    def _position_widgets(self):
        # Position nested widgets
        self.plot.grid()
