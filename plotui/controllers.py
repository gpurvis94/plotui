from model.grapher import ModelGrapher


class Controller(object):
    """
    The communication channel between the main window and the model.
    """
    def __init__(self, view):
        self.grapher = ModelGrapher()
        self.view = view

    ####################################################################
    #                        Artist properties                         #
    ####################################################################

    def get_plot_figure(self):
        return self.grapher.get_plot_figure()

    def set_title(self, title):
        self.grapher.set_axes_title(title)
        self.view.redraw_canvas()

    def set_xlabel(self, label):
        self.grapher.set_xlabel(label)
        self.view.redraw_canvas()

    def set_ylabel(self, label):
        self.grapher.set_ylabel(label)
        self.view.redraw_canvas()

    ####################################################################
    #                       Input data retrieval                       #
    ####################################################################

    def get_plot_function_strings(self):
        return self.grapher.get_plot_function_strings()

    def get_user_options(self, plot_type):
        return self.grapher.get_user_options(plot_type)

    def get_xvar_strings(self, plot_type):
        return self.grapher.get_xvar_strings(plot_type)

    def get_yvar_strings(self, plot_type):
        return self.grapher.get_yvar_strings(plot_type)

    ####################################################################
    #                             Plotting                             #
    ####################################################################

    def add_plot(self, key, plot_type):
        self.grapher.add_plot(key, plot_type)

    def update_plot(self, key):
        plot_args = self.view.get_plot_args(key)
        self.grapher.update_plot(key, plot_args)
        self.view.redraw_canvas()

    def delete_plot(self, key):
        self.grapher.delete_plot(key)
        self.view.redraw_canvas()

    ####################################################################
    #                        Axes limit methods                        #
    ####################################################################

    def scale_axis(self, xmin, xmax, ymin, ymax):
        """
        Sets the graph axis limts according to predefined variables
        """
        # Otherwise set limits
        self.grapher.set_axes_limits(xmin, xmax, ymin, ymax)
        self.view.redraw_canvas()

    def autoscale_axis(self):
        """
        Sets the graph axis limits according to max/min data values
        """
        self.grapher.set_axes_limits()
        self.view.redraw_canvas()
        return self.grapher.get_limits()

    ####################################################################
    #                            Exporting                             #
    ####################################################################

    def export(self, selected_index, file_name):
        # If export type is png image
        if selected_index == 0:
            file_name += '.png'
            self.view.export_png(file_name)
            
        # If export type is LaTeX data
        if selected_index == 1:
            file_name += '.dat'
            self.grapher.export_dat(file_name)

    ####################################################################
    #                         Error reporting                          #
    ####################################################################

    def message(self, title, message):
        self.view.message(title, message)
