import numpy as np
import matplotlib
from matplotlib.figure import Figure
matplotlib.use('TkAgg')


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
        if xdata is not None:
            self.xmin = np.min(xdata)
            self.xmax = np.max(xdata)
        if ydata is not None:
            self.ymin = np.min(ydata)
            self.ymax = np.max(ydata)


class PlotData(object):
    """
    Holds the axis data and line plot for each plotted line.
    """
    def __init__(self, plot_model, xdata, ydata, key=None, line=None):
        self.plot_model = plot_model
        self.xdata = xdata
        self.ydata = ydata
        self.line = line
        self.limits = AxesLimits()
        self.limits.update_limits_from_list(xdata=self.xdata, ydata=self.ydata)

    def update_plot_data(self, plot_args):
        """
        Calculates data using methods on the plot_model
        """
        self.xdata = self.plot_model.get_xdata(plot_args.x_var, plot_args.xmax,
                                               plot_args.xmin)
        self.ydata = self.plot_model.get_ydata(plot_args.y_var, plot_args.ymin,
                                               plot_args.ymax, self.xdata)


class ModelGrapher(object):
    """
    A class containing the OO interface for plotting from specific data
    structures, i.e. Model classes. Pyplot has not been used to make it
    simpler to customise the output for different backends.
    """
    def __init__(self, model):
        """
        :param Model_1 model: Reference to the model state information.
        """
        self.model = model

        # Instantiate and save references to matplotlib artists
        self._fig = Figure()
        self._axes = self._fig.add_subplot(111)
        self._plot_data = {}
        self._axes_limits = AxesLimits()

        # Set default titles and descriptions
        self._axes.set_title("Title")
        self._axes.set_xlabel("x axis")
        self._axes.set_ylabel("y axis")

    ####################################################################
    #                         Artist retrieval                         #
    ####################################################################

    def get_plot_figure(self):
        return self._fig

    ####################################################################
    #                       Getting/setting data                       #
    ####################################################################

    def update_plot_data(self, key, plot_args):
        # Update the plot data, remove the current line and then redraw
        self._plot_data[key].update_plot_data(plot_args)

        self._calc_axes_limits()
        self._plot_line(self._plot_data[key])

    def delete_plot(self, key):
        # Return and remove the line from the list and unplot it
        self._plot_data[key].line.remove()
        del self._plot_data[key]

        # Recalculate axis limits
        self._calc_axes_limits()

    ####################################################################
    #                             Plotting                             #
    ####################################################################

    def _plot_line(self, plot_data):
        """
        Plots a line to the canvas from a PlotData class.
        """
        # TODO when code vbuilds refactor to pass plot_data instead of key
        self.plot_data[key].line = self.axes.plot(
            self.plot_data[key].xdata,
            self.plot_data[key].ydata
            )

    ####################################################################
    #                        Axes limit methods                        #
    ####################################################################

    # TODO Rewruite/tiday
    def get_limits(self):
        return (self._axes_limits.xmin, self._axes_limits.xmax,
                self._axes_limits.ymin, self._axes_limits.ymax)

    def try_set_xlim(self, x_min=None, x_max=None):
        # Don't set limits if there is no data
        if len(self._xdata['x']) == 0:
            return False
        # If optional parameters are omitted, populate from stored data
        x_min = self._axes_limits.xmin if x_min is None else x_min
        x_max = self._axes_limits.xmax if x_max is None else x_max
        self.axes.set_xlim(x_min, x_max)
        return True

    def try_set_ylim(self, y_min=None, y_max=None):
        # Don't set limits if there is no data
        if len(self._plot_data) == 0:
            return False
        # If optional parameters are omitted, populate from stored data
        y_min = self._axes_limits.ymin if y_min is None else y_min
        y_max = self._axes_limits.ymax if y_max is None else y_max
        self.axes.set_ylim(y_min, y_max)
        return True

    def _calc_axes_limits(self):
        if len(self._xdata) == 0 or len(self._plot_data) == 0:
            return

        min_list = []
        max_list = []
        for key, val in self._xdata.items():
            min_list.append(np.min(val))
            max_list.append(np.max(val))

        self._axes_limits.xmin = np.min(min_list)
        self._axes_limits.xmax = np.max(max_list)

        min_list = []
        max_list = []
        for key, val in self._plot_data.items():
            min_list.append(np.min(val))
            max_list.append(np.max(val))

        self._axes_limits.ymin = np.min(min_list)
        self._axes_limits.ymax = np.max(max_list)

    def _calc_axis_limits(self, data, axis_min, axis_max):
        if len(data) == 0:
            return

        min_list = []
        max_list = []
        for key, val in data.items():
            min_list.append(np.min(val))
            max_list.append(np.max(val))

        axis_min[0] = np.min(min_list)
        axis_max[0] = np.max(max_list)
