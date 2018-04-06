from common import PlotType

class StraightLine(object):
    """
    A plot function for a horizontal line
    """
    variable_to_func = {
        'x': self._var_is_x,
        'y': self._var_is_y,
    }

    def __init__(self):
        # Set plot function information
        self.plot_type = PlotType.STRAIGHT_LINE
        self.plot_string = PlotType.to_string(self.plot_type)



    def get_xdata(self, x_var, xmin, xmax):
        """
        Maps user specified plot args to the appropriate function.
        """
        return _variable_to_func[x_var](xmin, xmax)

    def get_ydata(self, y_var, ymin, ymax, xdata):
        """
        Maps user specified plot args to the appropriate function.
        """
        return _variable_to_func[y_var](ymin, ymax)

    ####################################################################
    #                        Variable functions                        #
    ####################################################################

    def _var_is_x(self, xmin=None, xmax=None):
        return [xmin, xmax]

    def _var_is_y(self, ymin=None, ymax=None, xdata=None):
        return [ymin, ymax]
