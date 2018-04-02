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
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        # TODO change to a dictionary and save references to lines.
        # This will enable removal of specific lines rather than last.
        self.lines = []
        self.x_data = []
        self.y_data = []

        # Set default titles and descriptions
        self.axes.set_title("Title")
        self.axes.set_xlabel("x axis")
        self.axes.set_ylabel("y axis")

    def get_plot_figure(self):
        return self.fig

    def plot_model_line(self):
        self.x_data = np.arange(0.0, 10.0, 0.01)
        self.y_data = self.x_data**2
        self._plot_line(self.x_data, self.y_data)

    def _plot_line(self, data1, data2, param_dict=None):
        """
        A helper function to make a graph.
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
        self.lines.append(self.axes.plot(data1, data2, **param_dict))
        self.set_xlim()
        self.set_ylim()

    def remove_line(self):
        # Return and remove the line from the list and unplot it
        (line,) = self.lines.pop()
        line.remove()

    def set_xlim(self, x_min=None, x_max=None):
        if x_min is None:
            x_min = np.min(self.x_data)
        if x_max is None:
            x_max = np.max(self.x_data)
        self.axes.set_xlim(x_min, x_max)

    def set_ylim(self, y_min=None, y_max=None):
        if y_min is None:
            y_min = np.min(self.y_data)
        if y_max is None:
            y_max = np.max(self.y_data)
        self.axes.set_ylim(y_min, y_max)
