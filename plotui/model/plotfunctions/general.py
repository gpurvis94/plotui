import numpy as np

from common import PlotType, DisplayUserOptions


class BasePlotFunction(object):
    """
    The base class from which to inherit plot functions
    """
    def __init__(self, plot_type, user_option_args, xvar_strings, yvar_strings,
            variable_to_func):
        self.plot_type = plot_type
        self.plot_type_string = PlotType.to_string(self.plot_type)
        self.user_option_args = user_option_args
        self.xvar_strings = xvar_strings
        self.yvar_strings = yvar_strings
        self._variable_to_func = variable_to_func

    def get_data(self, var, var_min=None, var_max=None, var_data=None):
        """
        Maps user specified plot args to the appropriate function.
        """
        return self._variable_to_func[var](var_min, var_max, var_data)

class StraightLinePlotFunction(BasePlotFunction):
    """
    A plot function for a horizontal line
    """
    def __init__(self):
        super().__init__(
            plot_type=PlotType.STRAIGHT_LINE,
            user_option_args=DisplayUserOptions(True, True),
            xvar_strings=['x'],
            yvar_strings=['y'],
            variable_to_func={
                'x': self._var_is_x,
                'y': self._var_is_y,
                },
            )

    ####################################################################
    #                  Variable calculation functions                  #
    ####################################################################

    def _var_is_x(self, var_min, var_max, var_data):
        return np.linspace(var_min, var_max, 2)

    def _var_is_y(self, var_min, var_max, var_data):
        return np.linspace(var_min, var_max, 2)
