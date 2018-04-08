import numpy as np
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
matplotlib.use('TkAgg')


from common import PlotType
from model.plotfunctions.general import StraightLinePlotFunction
from model.plotfunctions.model1 import Model1PlotFunction


class AxesLimits(object):
    """
    Holds axis limit data and provides functionality for updating.
    """
    def __init__(self, xmin=0, xmax=0, ymin=0, ymax=0):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def update_limits_from_vals(self, xmin=None, xmax=None,
                                ymin=None, ymax=None):
        """
        Updates the limits from individual values.
        """
        if xmin is not None:
            self.xmin = xmin
        if xmax is not None:
            self.xmax = xmax
        if ymin is not None:
            self.ymin = ymin
        if ymax is not None:
            self.ymax = ymax

    def update_limits_from_list(self, xdata=None, ydata=None):
        """
        Updates the limits by calculating the max/min of a given range.
        """
        if xdata is not None and len(xdata) != 0:
            self.xmin = min(xdata)
            self.xmax = max(xdata)
        if ydata is not None and len(ydata) != 0:
            self.ymin = min(ydata)
            self.ymax = max(ydata)


class PlotData(object):
    """
    Holds the axis data and line plot for each plotted line.
    """
    def __init__(self, plot_model):
        self.plot_model = plot_model
        self.xdata = None
        self.ydata = None
        self.line = None
        self.limits = AxesLimits()

    def update_plot_data(self, plot_args):
        """
        Calculates data using methods on the plot_model
        """
        self.xdata = self.plot_model.get_data(plot_args.xvar, plot_args.xmin,
                                              plot_args.xmax)
        self.ydata = self.plot_model.get_data(plot_args.yvar, plot_args.ymin,
                                              plot_args.ymax, self.xdata)
        self.limits.update_limits_from_list(self.xdata, self.ydata)


class ModelGrapher(object):
    """
    A class containing the OO interface for plotting from specific data
    structures, i.e. Model classes. Pyplot has not been used to make it
    simpler to customise the output for different backends.
    """
    def __init__(self):
        self._load_plot_functions()
        self._load_artists()

        self._type_to_model = {
            PlotType.STRAIGHT_LINE: StraightLinePlotFunction,
            PlotType.MODEL_1: Model1PlotFunction,
        }

        # Set default titles and descriptions TODO move
        self._axes.set_title("Title")
        self._axes.set_xlabel("x axis")
        self._axes.set_ylabel("y axis")

    def _load_plot_functions(self):
        self._plot_functions = {}

        straight_line = StraightLinePlotFunction()
        model1 = Model1PlotFunction()

        self._plot_functions[straight_line.plot_type] = straight_line
        self._plot_functions[model1.plot_type] = model1

        self._plot_function_strings = []
        for key, val in self._plot_functions.items():
            self._plot_function_strings.append(val.plot_type_string)

    def _load_artists(self):
        self._fig = Figure()
        self._axes = self._fig.add_subplot(111)
        self._plot_data = {}
        self._axes_limits = AxesLimits()

    ####################################################################
    #                        Artist properties                         #
    ####################################################################

    def get_plot_figure(self):
        return self._fig

    def set_axes_title(self, title):
        self._axes.set_title(title)

    def set_xlabel(self, label):
        self._axes.set_xlabel(label)

    def set_ylabel(self, label):
        self._axes.set_ylabel(label)

    ####################################################################
    #                       Input data retrieval                       #
    ####################################################################

    def get_functions(self):
        return self._plot_function_strings

    def get_user_options(self, plot_type):
        return self._plot_functions[plot_type].user_option_args

    def get_xvar_strings(self, plot_type):
        return self._plot_functions[plot_type].xvar_strings

    def get_yvar_strings(self, plot_type):
        return self._plot_functions[plot_type].yvar_strings

    ####################################################################
    #                             Plotting                             #
    ####################################################################

    def add_plot(self, key, plot_type):
        self._plot_data[key] = PlotData(self._type_to_model[plot_type]())

    def update_plot(self, key, plot_args):
        # Update the plot data, remove the current line and then redraw
        if plot_args is not None:
            self._remove_line(key)
            self._plot_data[key].update_plot_data(plot_args)

            self._calc_all_axes_limits()
            self._plot_line(key)

    def delete_plot(self, key):
        # Return and remove the line from the list and unplot it
        self._remove_line(key)
        del self._plot_data[key]

        self._calc_all_axes_limits()

    def _remove_line(self, key):
        if self._plot_data[key].line is not None:
            (line,) = self._plot_data[key].line
            if line in self._axes.lines:
                line.remove()

    def _plot_line(self, key):
        """
        Plots a line to the canvas from a PlotData class.
        """
        # If the data is None (due to input error), remove current line
        if (len(self._plot_data[key].xdata) == 0
                or len(self._plot_data[key].ydata) == 0):
            return

        self._plot_data[key].line = self._axes.plot(
            self._plot_data[key].xdata,
            self._plot_data[key].ydata,
            )

    ####################################################################
    #                        Axes limit methods                        #
    ####################################################################

    def _calc_all_axes_limits(self):
        x = []
        y = []
        for key, val in self._plot_data.items():
            x.append(val.limits.xmin)
            x.append(val.limits.xmax)
            y.append(val.limits.ymin)
            y.append(val.limits.ymax)
        if len(x) == 0:
            x.append(0)
        if len(y) == 0:
            y.append(0)
        self._axes_limits.xmin = min(x)
        self._axes_limits.xmax = max(x)
        self._axes_limits.ymin = min(y)
        self._axes_limits.ymax = max(y)

    def get_limits(self):
        return (self._axes_limits.xmin, self._axes_limits.xmax,
                self._axes_limits.ymin, self._axes_limits.ymax)

    def set_axes_limits(self, xmin=None, xmax=None, ymin=None, ymax=None):
        if xmin is None:
            xmin = self._axes_limits.xmin
        if xmax is None:
            xmax = self._axes_limits.xmax
        if xmin == xmax:
            xmin -= 1
            xmax += 1
        self._axes.set_xlim(xmin, xmax)

        if ymin is None:
            ymin = self._axes_limits.ymin
        if ymax is None:
            ymax = self._axes_limits.ymax
        if ymin == ymax:
            ymin -= 1
            ymax += 1
        self._axes.set_ylim(ymin, ymax)

    ####################################################################
    #                            Exporting                             #
    ####################################################################

    def export_dat(self, file_name):
        f = open(file_name, "w+")
        f.write("x y\n")
        for key, val in self._plot_data.items():
            for i, x in enumerate(val.xdata):
                f.write(f'{x} {val.ydata[i]}\n')
            f.write("\n")
        f.close()

