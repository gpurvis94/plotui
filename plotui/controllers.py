from model import Model_1, ModelGrapher


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

    def plot_model_line(self):
        self.grapher.plot_model_line()
        self.view.redraw_canvas()

    def remove_line(self):
        self.grapher.remove_line()
        self.view.redraw_canvas()

    # Edit Axes

    def set_title(self, title):
        self.grapher.axes.set_title(title)
        self.view.redraw_canvas()

    def set_xlabel(self, label):
        self.grapher.axes.set_xlabel(label)
        self.view.redraw_canvas()

    def set_ylabel(self, label):
        self.grapher.axes.set_ylabel(label)
        self.view.redraw_canvas()
