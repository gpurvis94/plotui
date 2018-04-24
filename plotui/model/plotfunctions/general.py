import numpy as np

from common import PlotType, DisplayUserOptions


class BasePlotFunction(object):
    """
    The base class from which to inherit plot functions
    """
    def __init__(self):
        self._init_model_data()
        self._init_grapher_data()

    def _init_model_data(self):
        self.model = None

    def _init_grapher_data(self):
        self.plot_type
        self.plot_type_string
        self.user_option_args
        self.xvar_strings
        self.yvar_strings
        self.constant_strings = []
        self._x_var_to_func
        self._y_var_to_func

    def get_constant_vals(self):
        return self.model.get_constant_vals()

    def set_constant_vals(self, vals):
        return self.model.set_constant_vals(vals)

    def restore_defaults(self):
        self.model.restore_defaults()

    def get_xdata(self, var, var_min=None, var_max=None, var_data=None):
        return self._x_var_to_func[var](var_min, var_max, var_data)

    def get_ydata(self, var, var_min=None, var_max=None, var_data=None):
        return self._y_var_to_func[var](var_min, var_max, var_data)


class StraightLinePlotFunction(BasePlotFunction):
    """
    A plot function for a horizontal line
    """
    def _init_grapher_data(self):
        self.plot_type = PlotType.STRAIGHT_LINE
        self.plot_type_string = PlotType.to_string(self.plot_type)
        self.user_option_args = DisplayUserOptions(show_xrange=True,
            show_yrange=True)
        self.xvar_strings = ['x']
        self.yvar_strings =  ['y']
        self._x_var_to_func = {
            'x': self._var_is_x,
            }
        self._y_var_to_func = {
            'y': self._var_is_y,
            }

    ####################################################################
    #                  Variable calculation functions                  #
    ####################################################################

    def _var_is_x(self, var_min, var_max, var_data):
        return np.linspace(var_min, var_max, 2)

    def _var_is_y(self, var_min, var_max, var_data):
        return np.linspace(var_min, var_max, 2)
