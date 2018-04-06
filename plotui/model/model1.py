import numpy as np
import matplotlib
from matplotlib.figure import Figure
matplotlib.use('TkAgg')  # Must be done before importing pyplot


class Conversions:
    """
    A helper class for static conversion methods.
    """
    @staticmethod
    def mph_to_metres(value):
        """
        Converts a miles per hour value into a metres per second value.
        :param float value: The miles per hour value to be converted.
        :return float: The converted value.
        """
        return value*1609.34/3600


class BridgeSide(object):
    """
    A class detailing the properties of a single side of a bridge.
    """
    def __init__(self,
                 arrival_rate=10,
                 initial_queue=10,
                 ):
        self.Q = arrival_rate
        self.n_i = initial_queue
        self.tg = None
        self.tr = None


class GeneralProperties(object):
    """
    A class detailing the general properties pertaining to the bridge
    and both sides of the bridge.
    """
    def __init__(self,
                 bridge_length=20.0,
                 car_length=4.5,
                 separation_distance=2.0,
                 crossing_velocity=20.0,
                 ):
        """
        Sets the values. Default values will be used if not listed.
        :param float bridge_length: The length of the bridge, metres.
        :param float car_length: The length of an average car, metres.
        :param float separation_distance: Distance between cars, metres.
        :param float crossing_velocity: Crossing velocity, miles ph.
        """
        self.L = bridge_length
        self.l = car_length
        self.s = separation_distance
        self.v = Conversions.mph_to_metres(crossing_velocity)


class Model_1(object):  
    """
    A class containing model state information.
    """
    def __init__(self,
                 side=BridgeSide(),
                 props=GeneralProperties(),
                 ):
        """
        :param BridgeSide side: Both sides of the bridge data.
        :param GeneralProperties props: Non-side specific information.
        """
        # Save references to the 
        self.i = side
        self.j = side
        self.p = props

        # Calculate intial values of related params
        self.calc_tg(self.i)
        self.calc_tg(self.j)

    def calc_tg(self, s, p=None):
        """
        Calculates tg. Current limits are 30s < tg < 120s.
        :param BridgeSide s: The side for which to calculate tg.
        :param GeneralProperties p: The general data properties to use.
        """
        if p is None:
            p = self.p
        s.tg = np.log(s.n_i) + ((p.l + p.s)/p.v)*(s.n_i - 1)


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
    def __init__(self, key=None, xdata, ydata, line=None):
        self.xdata = xdata
        self.ydata = ydata
        self.line = line
        self.limits = AxesLimits()
        self.limits.update_limits_from_list(xdata=self.xdata, ydata=self.ydata)


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
        self._axes = self.fig.add_subplot(111)
        self._plot_data = {}
        self._axes_limits = AxesLimits()

        # Set default titles and descriptions
        self.axes.set_title("Title")
        self.axes.set_xlabel("x axis")
        self.axes.set_ylabel("y axis")

    ####################################################################
    #                         Artist retrieval                         #
    ####################################################################

    def get_plot_figure(self):
        return self.fig

    ####################################################################
    #                       Getting/setting data                       #
    ####################################################################

    def set_xdata(self, range_tup):
        self._xdata['x'] = np.arange(float(range_tup[0]), float(range_tup[1]), float(range_tup[2]))

    def edit_ydata_set(self, key):
        # Remove the current line from the graph and redraw
        if key in self._ydata:
            self.remove_data_set(key)
        self._ydata[key] = self._xdata['x']**np.pi * (np.random.rand() * 10)

        self._calc_axes_limits()
        self._plot_line(key)

    def remove_data_set(self, key):
        # Return and remove the line from the list and unplot it
        (line,) = self.lines.pop(key, None)
        line.remove()
        del self._ydata[key]
        self._calc_axes_limits()

    ####################################################################
    #                             Plotting                             #
    ####################################################################

    def _plot_line(self, ykey, param_dict=None):
        """
        A helper function to make a graph. TODO
        :param Axes ax: The axes to draw to.
        :param np.array data1: The x data.
        :param np.array data2: The y data.
        :param dict param_dict: Dictionary of kwargs to pass to ax.plot.
        :return list: List of artists added.
        """
        # Working around pythons dislike of mutable default arguments
        if param_dict is None:
            param_dict = {}
        # Plot the line and append the Line2D object to a list
        self.lines[ykey] = self.axes.plot(self._xdata['x'], self._ydata[ykey], **param_dict)

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
        if len(self._ydata) == 0:
            return False
        # If optional parameters are omitted, populate from stored data
        y_min = self._axes_limits.ymin if y_min is None else y_min
        y_max = self._axes_limits.ymax if y_max is None else y_max
        self.axes.set_ylim(y_min, y_max)
        return True

    def _calc_axes_limits(self):
        if len(self._xdata) == 0 or len(self._ydata) == 0:
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
        for key, val in self._ydata.items():
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
