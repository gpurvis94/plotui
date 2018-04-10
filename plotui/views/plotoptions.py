import tkinter as tk
import uuid

import views.styles as st
from common import PlotType, PlotArgs


class PlotOptionsFrame(st.SubFrame):
    """
    The visual design for the Plot element.
    """
    def _init_variables(self):
        self._plots = {}

    def _create_widgets(self):
        self._title_lbl = st.TitleLabel(self, "Plot Options")
        self._add_plot_btn = st.Button(self, "Add plot", self.add_plot)
        self._type_cmb = st.StringCombo(self, self._c.get_functions())
        self._plots_title_lbl = st.SubTitleLabel(self, text="Plots")

    def _position_widgets(self):
        self._title_lbl.grid(row=0, column=0, columnspan=2)
        self._add_plot_btn.grid(row=1, column=0, sticky='w')
        self._type_cmb.grid(row=1, column=1, sticky='w')
        self._plots_title_lbl.grid(row=2, column=0, sticky='w')

    def _configure_grid(self):
        self.grid_columnconfigure(1, weight=1)

    def add_plot(self):
        plot = PlotDataFrame(self, self._c,
            PlotType.str_to_plottype(self._type_cmb.get()))
        self._plots[plot.key] = plot
        self._c.add_plot(plot.key, plot.plot_type)
        plot.grid(sticky='w', columnspan=2, pady=2)

    def get_plot_args(self, key):
        try:
            return PlotArgs(
                self._plots[key].get_xvar(), self._plots[key].get_xmin(),
                self._plots[key].get_xmax(), self._plots[key].get_yvar(),
                self._plots[key].get_ymin(), self._plots[key].get_ymax(),
                )
        except tk.TclError:
            self._c.message("Error", "Range values must be a number.")


class PlotDataFrame(st.SubSubFrame):
    """
    The base class from which to inherit functionality
    """
    def __init__(self, parent, controller, plot_type):
        self.plot_type = plot_type
        super().__init__(parent, controller)

    def _init_variables(self):
        self._type_string = PlotType.to_string(self.plot_type)
        self.key = str(uuid.uuid4())

    def _create_widgets(self):
        self._type_lbl = st.Label(self, f'Plot type: "{self._type_string}"')
        # self._legend_ce = st.StringChkEnt(self, "Legend:", self._type_string)
        self._data_options = DataOptionsFrame(self, self._c, self.plot_type)
        self._actions = PlotActionsFrame(self, self._c)

    def _position_widgets(self):
        self._type_lbl.grid(row=0, column=0)
        self._data_options.grid(row=0, column=1, sticky='w')
        # self._legend_ce.grid(row=1, column=1, sticky='w') 
        self._actions.grid(row=2, column=1, sticky='w')

    def get_xvar(self):
        return self._data_options.xvar_cmb.get()

    def get_xmin(self):
        if self._data_options.display_user_optionns.show_xrange:
            return self._data_options.xrange.min_entry.get()

    def get_xmax(self):
        if self._data_options.display_user_optionns.show_xrange:
            return self._data_options.xrange.max_entry.get()

    def get_yvar(self):
        return self._data_options.yvar_cmb.get()

    def get_ymin(self):
        if self._data_options.display_user_optionns.show_yrange:
            return self._data_options.yrange.min_entry.get()

    def get_ymax(self):
        if self._data_options.display_user_optionns.show_yrange:
            return self._data_options.yrange.max_entry.get()

class DataOptionsFrame(st.SubSubFrame):
    """
    A frame which holds widgets that the user interacts with to set
    data options. The model is responsible for determining which options
    are gridded.
    """
    def __init__(self, parent, controller, plot_type):
        self._type = plot_type
        super().__init__(parent, controller)

    def _create_widgets(self):
        self._xvar_lbl = st.Label(self, 'X variable:')
        self.xvar_cmb = st.StringCombo(self, self._c.get_xvars(self._type))
        self._yvar_lbl = st.Label(self, 'Y variable:')
        self.yvar_cmb = st.StringCombo(self, self._c.get_yvars(self._type))
        
    def _position_widgets(self):
        self._xvar_lbl.grid(row=0, column=0, sticky='w')
        self.xvar_cmb.grid(row=0, column=1, sticky='w')
        self._yvar_lbl.grid(row=0, column=3, sticky='w')
        self.yvar_cmb.grid(row=0, column=4, sticky='w')

    def _create_optional_widgets(self):
        self.display_user_optionns = self._c.get_user_options(self._type)

        if self.display_user_optionns.show_xrange:
            self.xrange = PlotRangeFrame(self, self._c)
            self.xrange.grid(row=0, column=2, sticky='w')

        if self.display_user_optionns.show_yrange:
            self.yrange = PlotRangeFrame(self, self._c)
            self.yrange.grid(row=0, column=5)


class PlotRangeFrame(st.SubSubFrame):
    """
    A widget that allows the user to specify the axis data range.
    """
    def _create_widgets(self):
        self._description_lbl = st.Label(self, "Range:")
        self.min_entry = st.FloatEntry(self, 0)
        self._to_lbl = st.Label(self, 'to')
        self.max_entry = st.FloatEntry(self, 0)

    def _position_widgets(self):
        self._description_lbl.grid(row=0, column=0, sticky='w')
        self.min_entry.grid(row=0, column=1, sticky='w')
        self._to_lbl.grid(row=0, column=2, sticky='w')
        self.max_entry.grid(row=0, column=3, sticky='w')

    def _pad_columns(self):
        pass


class PlotActionsFrame(st.SubSubFrame):
    """
    A widget that contains the buttons that allow the user to show,
    update, or delete a plot.
    """
    def _create_widgets(self):
        self._show_plot_chk = st.BoolCheck(self, "Show plot:", True)
        self._update_btn = st.Button(self, "Redraw plot", self.update_plot)
        self._remove_btn = st.Button(self, "Remove plot", self.delete_plot)

    def _position_widgets(self):
        self._show_plot_chk.grid(row=0, column=0)
        self._update_btn.grid(row=0, column=1)
        self._remove_btn.grid(row=0, column=2)

    def update_plot(self):
        self._c.update_plot(self._parent.key)

    def delete_plot(self):
        self._c.delete_plot(self._parent.key)
        self._parent.destroy()

