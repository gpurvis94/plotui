from enum import Enum, auto


class PlotType(Enum):
    STRAIGHT_LINE = auto()
    MODEL_1 = auto()
    MODEL_2 = auto()

    @staticmethod
    def to_string(plot_type):
        if _plottype_to_str is not None:
            return _plottype_to_str[plot_type]

    @staticmethod
    def str_to_plottype(string):
        if _str_to_plottype is not None:
            return _str_to_plottype[string]

# TODO Include mapping for None: None? Test if works
_plottype_to_str = {
    PlotType.STRAIGHT_LINE: 'Straight line',
    PlotType.MODEL_1: 'Model 1',
    PlotType.MODEL_2: 'Model 2',
}

_str_to_plottype = {
    'Straight line': PlotType.STRAIGHT_LINE,
    'Model 1': PlotType.MODEL_1,
    'Model 2': PlotType.MODEL_2,
}


class PlotArgs(object):
    """
    Stores information the user can specify for plotting.
    """
    def __init__(self, xvar=None, xmin=None, xmax=None, yvar=None, ymin=None,
            ymax=None):
        self.xvar = xvar
        self.xmin = xmin
        self.xmax = xmax
        self.yvar = yvar
        self.ymin = ymin
        self.ymax = ymax


class DisplayUserOptions(object):
    """
    Defines which data option widgets to display.
    """
    def __init__(self, show_xrange=False, show_yrange=False, show_set_constants=False):
        self.show_xrange = show_xrange
        self.show_yrange = show_yrange
        self.show_set_constants = show_set_constants
