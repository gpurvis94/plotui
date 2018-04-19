from model.grapher import ModelGrapher


class Controller(object):
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

    def get_functions(self):
        return self.grapher.get_functions()

    def get_user_options(self, plot_type):
        return self.grapher.get_user_options(plot_type)

    def get_xvars(self, plot_type):
        return self.grapher.get_xvar_strings(plot_type)

    def get_yvars(self, plot_type):
        return self.grapher.get_yvar_strings(plot_type)

    ####################################################################
    #                        Editing constants                         #
    ####################################################################

    def set_const(self, key, plot_type):
        self.view.init_set_constants_window(key, plot_type)

    def get_constant_strings(self, plot_type):
        return self.grapher.get_constant_strings(plot_type)

    def get_constant_vals(self, key):
        return self.grapher.get_constant_vals(key)

    def save_entry_vals(self, key, vals):
        self.grapher.set_constant_vals(key, vals)

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
        self.grapher.set_axes_limits(xmin, xmax, ymin, ymax)
        self.view.redraw_canvas()

    def autoscale_axis(self):
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
            self.message("Success", "Exported image.")
            
        # If export type is LaTeX data
        if selected_index == 1:
            file_name += '.dat'
            self.grapher.export_dat(file_name)
            self.message("Success", "Exported data.")


    ####################################################################
    #                         Error reporting                          #
    ####################################################################

    def message(self, title, message):
        self.view.message(title, message)
