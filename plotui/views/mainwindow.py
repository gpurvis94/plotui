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
        self.parent = parent
        self.c = Controller(self)

        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self):
        # Instantiate nested widgets
        self.plot = PlotFrame(self, self.c)
        self.graph_options = GraphOptionsFrame(self, self.c)
        self.export_options = ExportOptionsFrame(self, self.c)
        self.plot_options = PlotOptionsFrame(self, self.c)

    def _position_widgets(self):
        # Position nested widgets

        # Row 0
        self.graph_options.grid(row=0, column=0, sticky="nsew")
        self.plot.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Row 1
        self.export_options.grid(row=1, column=0, sticky="nsew")

        # Row 2
        self.plot_options.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Configure base grid layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def redraw_canvas(self):
        self.plot.canvas.draw()