import tkinter as tk
from tkinter import ttk
import uuid

from views.styles import BlueButton
from common import PlotType, PlotArgs


class PlotOptionsFrame(ttk.Frame):
    """
    The visual design for the Plot element.
    """
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style='Sub.TFrame', border=5)
        self._c = controller
        self._plots = {}

        self._init_variables()
        self._create_widgets()
        self._position_widgets()

    def _init_variables(self):
        self._plot_type_strings = self._c.get_plot_function_strings()
        self._selected_type = tk.StringVar(value=self._plot_type_strings[0])

    def _create_widgets(self):
        self._main_title_lbl = ttk.Label(self, text="Plot Options",
            style='Title.TLabel')
        self._add_plot_btn = BlueButton(master=self, text="Add plot",
            command=self._add_plot)
        self._plot_type_combo = ttk.Combobox(self, width=15,
            textvariable=self._selected_type, values=self._plot_type_strings)
        self._plots_title_lbl = ttk.Label(self, text="Plots",
            style='SubTitle.TLabel')

    def _position_widgets(self):
        self._main_title_lbl.grid(row=0, column=0)
        self._add_plot_btn.grid(row=1, column=0, sticky='w', pady=1)
        self._plot_type_combo.grid(row=1, column=1, sticky='w', pady=1)
        self._plots_title_lbl.grid(row=2, column=0, sticky='w')

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

    def _add_plot(self):
        """
        Adds a plot data set widget according to the type specified
        """
        plot = DataOptionsFrame(self, self._c,
            PlotType.str_to_plottype(self._selected_type.get()))
        self._plots[plot.key] = plot
        self._c.add_plot(plot.key, plot.plot_type)
        plot.grid(sticky='w', columnspan=2, pady=1)

    ####################################################################
    #                     Controller communication                     #
    ####################################################################

    def get_plot_args(self, key):
        try:
            return PlotArgs(
                xvar=self._plots[key].get_xvar(),
                xmin=self._plots[key].get_xmin(),
                xmax=self._plots[key].get_xmax(),
                yvar=self._plots[key].get_yvar(),
                ymin=self._plots[key].get_ymin(),
                ymax=self._plots[key].get_ymax(),
                )
            return plot_args
        except tk.TclError:
            self._c.report_error("Range values must be a number.")


class DataOptionsFrame(ttk.Frame):
    """
    The base class from which to inherit functionality
    """
    def __init__(self, parent, controller, plot_type):
        ttk.Frame.__init__(self, parent)
        self._c = controller
        self.plot_type = plot_type
        self._plot_type_string = PlotType.to_string(plot_type)
        self.key = str(uuid.uuid4())

        self._init_variables()
        self._create_widgets()
        self._position_widgets()

    def _init_variables(self):
        self._is_legend = tk.BooleanVar(value=False)
        self._legend_txt = tk.StringVar(value="Straight line")

    def _create_widgets(self):
        self._plot_type_lbl = ttk.Label(master=self,
            text='Plot type: "%s"    ' % self._plot_type_string)
        self._legend_chkbtn = ttk.Checkbutton(self, onvalue=True,
            text="Legend: ", variable=self._is_legend)
        self._legend_entry = ttk.Entry(master=self, width=15,
            textvariable=self._legend_txt)
        self._plot_data_options = UserDataOptionsFrame(
            self, self._c, self.plot_type)
        self._actions = PlotActionsFrame(self, self._c)

    def _position_widgets(self):
        self._plot_type_lbl.grid(row=0, column=0)
        self._legend_chkbtn.grid(row=0, column=1)
        self._legend_entry.grid(row=0, column=2)
        self._plot_data_options.grid(row=0, column=3)
        self._actions.grid(row=1, column=1, columnspan=3, sticky='w', pady=2)

    def get_xvar(self):
        return self._plot_data_options.selected_xvar.get()

    def get_xmin(self):
        if self._plot_data_options.display_user_optionns.show_xrange:
            return self._plot_data_options.xrange.min.get()

    def get_xmax(self):
        if self._plot_data_options.display_user_optionns.show_xrange:
            return self._plot_data_options.xrange.max.get()

    def get_yvar(self):
        return self._plot_data_options.selected_yvar.get()

    def get_ymin(self):
        if self._plot_data_options.display_user_optionns.show_yrange:
            return self._plot_data_options.yrange.min.get()

    def get_ymax(self):
        if self._plot_data_options.display_user_optionns.show_yrange:
            return self._plot_data_options.yrange.max.get()

class UserDataOptionsFrame(ttk.Frame):
    """
    A frame which holds widgets that the user interacts with to set
    data options. The model is responsible for determining which options
    are gridded.
    """
    def __init__(self, parent, controller, plot_type):
        ttk.Frame.__init__(self, parent)
        self._c = controller
        self._plot_type = plot_type

        self._init_variables()
        self._create_widgets()
        self._position_widgets()
        self._create_optional_widgets()

    def _init_variables(self):
        self._xvar_strings = self._c.get_xvar_strings(self._plot_type)
        self.selected_xvar = tk.StringVar(value=self._xvar_strings[0])
        self._yvar_strings = self._c.get_yvar_strings(self._plot_type)
        self.selected_yvar = tk.StringVar(value=self._yvar_strings[0])

    def _create_widgets(self):
        self._xvar_lbl = ttk.Label(master=self, text='    X variable:')
        self._xvar_combo = ttk.Combobox(master=self, width=15,
            textvariable=self.selected_xvar, values=self._xvar_strings)
        self._yvar_lbl = ttk.Label(master=self, text='    Y variable:')
        self._yvar_combo = ttk.Combobox(master=self, width=15,
            textvariable=self.selected_yvar, values=self._yvar_strings)
        
    def _position_widgets(self):
        self._xvar_lbl.grid(row=0, column=0, sticky='w')
        self._xvar_combo.grid(row=0, column=1, sticky='w')
        self._yvar_lbl.grid(row=0, column=3, sticky='w')
        self._yvar_combo.grid(row=0, column=4, sticky='w')

    def _create_optional_widgets(self):
        self.display_user_optionns = self._c.get_user_options(self._plot_type)

        if self.display_user_optionns.show_xrange:
            self.xrange = PlotRangeFrame(self, self._c, message="    Range:")
            self.xrange.grid(row=0, column=2, sticky='w')

        if self.display_user_optionns.show_yrange:
            self.yrange = PlotRangeFrame(self, self._c, message="    Range:")
            self.yrange.grid(row=0, column=5)


class PlotRangeFrame(ttk.Frame):
    """
    A widget that allows the user to specify the axis data range.
    """
    def __init__(self, parent, controller, message):
        ttk.Frame.__init__(self, parent)
        self._c = controller

        self._init_variables()
        self._create_widgets(message)
        self._position_widgets()

    def _init_variables(self):
        self.min = tk.DoubleVar(value=0)
        self.max = tk.DoubleVar(value=0)

    def _create_widgets(self, message):
        self._description_lbl = ttk.Label(self, text=message)
        self._min_entry = ttk.Entry(master=self, width=5,
                                       textvariable=self.min)
        self._to_lbl = ttk.Label(master=self, text='to')
        self._max_entry = ttk.Entry(master=self, width=5,
                                       textvariable=self.max)

    def _position_widgets(self):
        self._description_lbl.grid(row=0, column=0, sticky='w')
        self._min_entry.grid(row=0, column=1, sticky='w')
        self._to_lbl.grid(row=0, column=2, sticky='w')
        self._max_entry.grid(row=0, column=3, sticky='w')


class PlotActionsFrame(ttk.Frame):
    """
    A widget that contains the buttons that allow the user to show,
    update, or delete a plot.
    """
    def __init__(self, parent, controller):
        # Initialize frame
        ttk.Frame.__init__(self, parent)
        self._c = controller
        self._parent = parent

        # Create and position widgets
        self._init_variables()
        self._create_widgets()
        self._position_widgets()

    def _init_variables(self):
        self._is_show_plot = tk.BooleanVar(value=True)

    def _create_widgets(self):
        self._show_plot_chk = ttk.Checkbutton(self, onvalue=True,
            text="Show plot", variable=self._is_show_plot)
        self._update_plot_btn = BlueButton(master=self, text="Redraw plot",
            command=self.update_plot)
        self._remove_plot_btn = BlueButton(master=self, text="Remove plot",
            command=self.delete_plot)

    def _position_widgets(self):
        self._show_plot_chk.grid(row=0, column=0, padx=2)
        self._update_plot_btn.grid(row=0, column=1, padx=2)
        self._remove_plot_btn.grid(row=0, column=2, padx=2)

    ####################################################################
    #                             Commands                             #
    ####################################################################

    def update_plot(self):
        self._c.update_plot(self._parent.key)

    def delete_plot(self):
        self._c.delete_plot(self._parent.key)
        self._parent.destroy()

