from model.model1 import Model_1, ModelGrapher


class Controller(object):
    """
    The communication channel between the main window and the model.
    """
    def __init__(self, view):
        # Instantiate model/view components
        self.model = Model_1()
        self.grapher = ModelGrapher(self.model)
        self.view = view

    def get_plot_figure(self):
        return self.grapher.get_plot_figure()

    # Data set functions

    def set_xdata(self, range_tup):
        self.grapher.set_xdata(range_tup)

    def edit_data_set(self, key):
        self.grapher.edit_ydata_set(key)
        self.view.redraw_canvas()

    def remove_data_set(self, key):
        self.grapher.remove_data_set(key)
        self.view.redraw_canvas()

    # Title methods

    def set_title(self, title):
        self.grapher.axes.set_title(title)
        self.view.redraw_canvas()

    # Axis label methods

    def set_xlabel(self, label):
        self.grapher.axes.set_xlabel(label)
        self.view.redraw_canvas()

    def set_ylabel(self, label):
        self.grapher.axes.set_ylabel(label)
        self.view.redraw_canvas()

    # Axis scaling methods

    def scale_axis(self, x_min, x_max, y_min, y_max):
        """
        Sets the graph axis limts according to predefined variables
        :param float x_min: The x lower bound. 
        :param float x_man: The x upper bound.
        :param float y_min: The y lower bound.
        :param float y_man: The y upper bound.
        """
        # Otherwise set limits
        self.grapher.try_set_xlim(x_min, x_max)
        self.grapher.try_set_ylim(y_min, y_max)
        self.view.redraw_canvas()

    def autoscale_axis(self):
        """
        Sets the graph axis limits according to max/min data values
        """
        # If setting the axis limits was unsuccessful, return None
        if not self.grapher.try_set_xlim() or not self.grapher.try_set_ylim():
            return None
        self.view.redraw_canvas()
        # Return values so the entry boxes can be updated
        return self.grapher.get_limits()
