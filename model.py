import numpy as np
import matplotlib
from matplotlib.figure import Figure
matplotlib.use('TkAgg')  # Must be done before importing pyplot
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


class SystemProperties(object):
    """
    A class that describes the system state
    """
    def __init__(self, side_i, side_j, props):
        self.side_i = side_i
        self.side_j = side_j
        self.props = props


class Model_1(object):
    def __init__(self,
                 side_i=BridgeSide(),
                 side_j=BridgeSide(),
                 props=GeneralProperties(),
                 ):
        self.i = side_i
        self.j = side_j
        self.props = props

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.lines = []

    def plot_line(self, data1, data2, param_dict=None):
        """
        A helper function to make a graph.
        :param ax: The axes to draw to.
        :type ax: Axes
        :param data1: The x data.
        :type data1: np.array
        :param data2: The y data.
        :type data2: np.array
        :param param_dict: Dictionary of kwargs to pass to ax.plot.
        :type param_dict: dict
        :return: List of artists added.
        :rtype: list
        """
        # Working around pythons dislike of mutable default arguments
        if param_dict is None:
            param_dict = {}
        self.lines.append(self.axes.plot(data1, data2, **param_dict))

    def remove_line(self):
        line = self.lines.pop()
        line.remove()


model = Model_1()

x = np.arange(0.0, 5.0, 0.01)
a = x**2
b = x**3
model.plot_line(x, a)
model.plot_line(x, b)

# FOR THE GUI

root = tk.Tk()
canvas = FigureCanvasTkAgg(model.fig, root)
widget = canvas.get_tk_widget()
widget.grid()
root.mainloop()

