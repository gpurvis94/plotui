from tkinter import messagebox
from tkinter import ttk

from controllers import Controller
from views.graphoptions import GraphOptionsFrame
from views.exportoptions import ExportOptionsFrame
from views.plotoptions import PlotOptionsFrame
from views.plot import PlotFrame


class MainWindowFrame(ttk.Frame):
    """
    The container frame for the main window.
    """
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, border=4, style='Main.TFrame')
        self._parent = parent
        self._c = Controller(self)

        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self):
        # Instantiate nested widgets
        self._plot = PlotFrame(self, self._c)
        self._graph_options = GraphOptionsFrame(self, self._c)
        self._export_options = ExportOptionsFrame(self, self._c)
        self._plot_options = PlotOptionsFrame(self, self._c)

    def _position_widgets(self):
        # Position nested widgets

        # Row 0
        self._graph_options.grid(row=0, column=0, sticky="nsew")
        self._plot.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Row 1
        self._export_options.grid(row=1, column=0, sticky="nsew")

        # Row 2
        self._plot_options.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Configure base grid layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def redraw_canvas(self):
        self._plot.redraw_canvas()

    def get_plot_args(self, key):
        return self._plot_options.get_plot_args(key)

    ####################################################################
    #                            Exporting                             #
    ####################################################################

    def export_png(self, file_name):
        self._plot.export_png(file_name)

    ####################################################################
    #                         Error reporting                          #
    ####################################################################

    def message(self, title, message):
        """
        Displays a messagebox with an error message.
        """
        messagebox.showinfo(title, message)