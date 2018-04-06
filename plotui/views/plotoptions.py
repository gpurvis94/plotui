import tkinter as tk
from tkinter import ttk
import uuid

from views.styles import BlueButton
from common import PlotType


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
        self._selected_type = tk.StringVar(value='Straight line')
        self._plot_type_to_widget = {
            'Straight line': PlotOptions1,
            'Model 1': "TODO",
            }
        # TODO Change this to get the types of stuff from controller
        self._plot_type_list = ('Straight line', 'More lines')

    def _create_widgets(self):
        self._main_title_lbl = ttk.Label(self, text="Plot Options",
            style='Title.TLabel')
        self._add_plot_btn = BlueButton(master=self, text="Add plot",
            command=self._add_plot)
        self._plot_type_combo = ttk.Combobox(self, width=15,
            textvariable=self._selected_type, values=self._plot_type_list)
        self._plots_title_lbl = ttk.Label(self, text="Plots",
            style='SubTitle.TLabel')

    def _position_widgets(self):
        self._main_title_lbl.grid(row=0, column=0)
        self._add_plot_btn.grid(row=1, column=0, sticky='w', pady=1)
        self._plot_type_combo.grid(row=1, column=1, sticky='w', pady=1)
        self._plots_title_lbl.grid(row=2, column=0, sticky='w')

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

    ####################################################################
    #                          Editing plots                           #
    ####################################################################

    def _add_plot(self):
        """
        Adds a plot data set widget according to the type specified
        """
        # If the selected plot is not recognised report error
        if self._selected_type.get() not in self._plot_type_to_widget.keys():
            self._c.report_error(
                f'Unknown plot type: "{self._selected_type.get()}".')
            return

        plot = self._plot_type_to_widget[self._selected_type.get()](
            self, self._c, self._selected_type.get())
        self._plots[plot.key] = plot
        plot.grid(sticky='w', columnspan=2, pady=1)


class BaseDataOptionsFrame(ttk.Frame):
    """
    The base class from which to inherit functionality
    """
    def __init__(self, parent, controller, plot_type):
        ttk.Frame.__init__(self, parent)
        self._c = controller
        self._plot_type = plot_type
        self._key = str(uuid.uuid4())

        self._init_variables()
        self._create_widgets()
        self._position_widgets()

    def _init_variables(self):
        self._is_legend = tk.BooleanVar(value=False)
        self._legend_txt = tk.StringVar(value="Straight line")

    def _create_widgets(self):
        self._plot_type_lbl = ttk.Label(master=self,
            text='Plot type: "%s"    ' % self._plot_type)
        self._legend_chkbtn = ttk.Checkbutton(self, onvalue=True,
            text="Legend: ", variable=self._is_legend)
        self._legend_entry = ttk.Entry(master=self, width=15,
            textvariable=self._legend_txt)
        self._plot_data_options = PlotDataOptions1(self, self._c)
        self._actions = PlotActionsFrame(self, self._c)

    def _position_widgets(self):
        self._plot_type_lbl.grid(row=0, column=0)
        self._legend_chkbtn.grid(row=0, column=1)
        self._legend_entry.grid(row=0, column=2)
        self._plot_data_optionslo.grid(row=0, column=3)
        self._actions.grid(row=0, column=4)

# TODO work out whether to inherit sort out the dictionary ahh
class TwoRange_DataOptionsFrame(ttk.Frame):
    """
    A frame which holds customisable options for setting axis data sets.
    """
    def __init__(self, parent, controller):
        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self):
        self._x_range = PlotRangeFrame(self, self._c,
            message="    X range: ")
        self._y_range = PlotRangeFrame(self, self._c,
            message="    Y range: ")

    def _position_widgets(self):
        self._x_range.grid(row=0, column=0)
        self._y_range.grid(row=0, column=1)


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
        self._min = tk.StringVar(value=0)
        self._max = tk.StringVar(value=0)

    def _create_widgets(self, message):
        self._description_lbl = ttk.Label(self, text=message)
        self._min_entry = ttk.Entry(master=self, width=5,
                                       textvariable=self._min)
        self._to_lbl = ttk.Label(master=self, text='to')
        self._max_entry = ttk.Entry(master=self, width=5,
                                       textvariable=self._max)

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
        self._c.edit_data_set(self._parent.key)

    def delete_plot(self):
        self._c.delete_plot(self._parent.key)
        self._parent.destroy()

