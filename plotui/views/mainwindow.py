from tkinter import messagebox

from controllers import Controller
import views.styles as st
from views.graphoptions import GraphOptionsFrame
from views.exportoptions import ExportOptionsFrame
from views.plotoptions import PlotOptionsFrame
from views.plot import PlotFrame


class MainWindowFrame(st.MainFrame):
    """
    The container frame for the main window.
    """
    def __init__(self, parent):
        self._c = Controller(self)
        super().__init__(parent, self._c)

    def _create_widgets(self):
        self._plot = PlotFrame(self, self._c)
        self._graph_options = GraphOptionsFrame(self, self._c)
        self._export_options = ExportOptionsFrame(self, self._c)
        self._plot_options = PlotOptionsFrame(self, self._c)

    def _position_widgets(self):
        self._graph_options.grid(row=0, column=0, sticky="nsew")
        self._plot.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self._export_options.grid(row=1, column=0, sticky="nsew")
        self._plot_options.grid(row=2, column=0, columnspan=2, sticky="nsew")

    def _configure_grid(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def redraw_canvas(self):
        self._plot.redraw_canvas()

    def get_plot_args(self, key):
        return self._plot_options.get_plot_args(key)

    def export_png(self, file_name):
        self._plot.export_png(file_name)

    def message(self, title, message):
        messagebox.showinfo(title, message)