import numpy as np

from common import PlotType, DisplayUserOptions


class BasePlotFunction(object):
    """
    The base class from which to inherit plot functions
    """
    def __init__(self):
        self._init_grapher_data()
        self._init_model_data()

    def _init_grapher_data(self):
        self.plot_type
        self.plot_type_string
        self.user_option_args
        self.xvar_strings
        self.yvar_strings
        self._variable_to_func

    def _init_model_data(self):
        pass

    def restore_defaults(self):
        pass

    def get_data(self, var, var_min=None, var_max=None, var_data=None):
        """
        Maps user specified plot args to the appropriate function.
        """
        return self._variable_to_func[var](var_min, var_max, var_data)


class StraightLinePlotFunction(BasePlotFunction):
    """
    A plot function for a horizontal line
    """
    def _init_grapher_data(self):
        self.plot_type = PlotType.STRAIGHT_LINE
        self.plot_type_string = PlotType.to_string(self.plot_type)
        self.user_option_args = DisplayUserOptions(True, True)
        self.xvar_strings = ['x']
        self.yvar_strings =  ['y']
        self._variable_to_func = {
            'x': self._var_is_x,
            'y': self._var_is_y,
            }

    ####################################################################
    #                  Variable calculation functions                  #
    ####################################################################

    def _var_is_x(self, var_min, var_max, var_data):
        return np.linspace(var_min, var_max, 2)

    def _var_is_y(self, var_min, var_max, var_data):
        return np.linspace(var_min, var_max, 2)
