from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from views.styles import SubFrame


class PlotFrame(SubFrame):
    """
    The visual design for the Plot frame.
    """
    def _create_widgets(self):
        self._canvas = FigureCanvasTkAgg(self._c.get_plot_figure(), self)
        self._plot = self._canvas.get_tk_widget()

    def _position_widgets(self):
        self._plot.grid()

    def redraw_canvas(self):
        self._canvas.draw()

    def export_png(self, file_name):
        self._canvas.print_png(file_name)
