import tkinter as tk
from tkinter import ttk
import uuid

from views.styles import BlueButton


class PlotOptionsFrame(ttk.Frame):
    """
    The visual design for the Plot element.
    """
    def __init__(self, parent, controller):
        # Initialize frame
        ttk.Frame.__init__(self, parent, style='Sub.TFrame', border=5)
        self.c = controller
        self.dynamic_yaxis_data_set = []

        # Create and position widgets
        self._create_widgets()
        self._position_widgets()
        self._add_axis_data_set()

    def _create_widgets(self):
        # Instantiate nested widgets
        self.main_title_lbl = ttk.Label(self, text="Plot Options",
                                        style='Title.TLabel')
        self.xaxis_title_lbl = ttk.Label(self, text="X axis data set",
                                         style='SubTitle.TLabel')
        self.udpate_xdata_btn = BlueButton(master=self, text="Update x data",
                                           command=self._update_xdata)
        self.xaxis_data_set = AxisDataSet(self, self.c, key=0)
        self.yaxis_title_lbl = ttk.Label(self, text="Y axis data sets",
                                         style='SubTitle.TLabel')
        self.add_data_set_btn = BlueButton(master=self, text="Add data set",
                                           command=self._add_axis_data_set)

        # TODO add button below y axis data set for adding y axis plots
        # list y axis plots as alistbox
        # # inherit from AxisDataSet

    def _position_widgets(self):
        # Position nested widgets
        self.main_title_lbl.grid(row=0, column=0)
        self.xaxis_title_lbl.grid(row=1, column=0, sticky='w')
        self.udpate_xdata_btn.grid(row=2, column=0, sticky='w', pady=1)
        self.xaxis_data_set.grid(row=3, column=0, sticky='w', pady=1)
        self.yaxis_title_lbl.grid(row=4, column=0, sticky='w')
        self.add_data_set_btn.grid(row=5, column=0, sticky='w', pady=1)

        # Configure rows and columns
        self.grid_columnconfigure(0, weight=1)

    def _update_xdata(self):
        range_tup = self.xaxis_data_set.get_range()
        self.c.set_xdata(range_tup)

    def _add_axis_data_set(self):
        yaxis_data_set = YAxisDataSet(self, self.c)
        self.dynamic_yaxis_data_set.append(yaxis_data_set)
        yaxis_data_set.grid(sticky='w', pady=1)


class AxisDataSet(ttk.Frame):
    """
    A frame chich holds customisable options for setting axis data sets.
    """
    def __init__(self, parent, controller, key=None):
        # Initialize frame
        ttk.Frame.__init__(self, parent)
        self.c = controller
        if key is None:
            key = str(uuid.uuid4())
        self.key = key

        # Create and position widgets/variables
        self._init_variables()
        self._create_widgets()
        self._position_widgets()

    def _init_variables(self):
        # Instantiate widget variables
        self.variable_list = ("one", "two", "three")
        self.var_min = tk.StringVar(value=0)
        self.var_max = tk.StringVar(value=1)
        self.var_interval = tk.StringVar()

    def _create_widgets(self):
        # Instantiate nested widgets
        self.var_lbl = ttk.Label(master=self, text='Model variable:')
        self.var_combo = ttk.Combobox(self, width=10,
                                      values=self.variable_list)
        self.range_lbl = ttk.Label(master=self, text='    Range:')
        self.var_min_entry = ttk.Entry(master=self, width=5,
                                       textvariable=self.var_min)
        self.to_lbl = ttk.Label(master=self, text='to')
        self.var_max_entry = ttk.Entry(master=self, width=5,
                                       textvariable=self.var_max)
        self.interval_lbl = ttk.Label(master=self, text='    Interval:')
        self.var_interval_entry = ttk.Entry(master=self, width=5,
                                            textvariable=self.var_interval)

    def _position_widgets(self):
        # Position nested widgets
        self.var_lbl.grid(row=0, column=0)
        self.var_combo.grid(row=0, column=1)
        self.range_lbl.grid(row=0, column=2)
        self.var_min_entry.grid(row=0, column=3)
        self.to_lbl.grid(row=0, column=4)
        self.var_max_entry.grid(row=0, column=5)
        self.interval_lbl.grid(row=0, column=6)
        self.var_interval_entry.grid(row=0, column=7)

    def get_range(self):
        return (self.var_min.get(), self.var_max.get(),
                self.var_interval.get())


class YAxisDataSet(AxisDataSet):    # TODO - store x axis data for each line
    """
    A frame which holds customisable options for setting multiple data
    sets for the y axis.
    """
    def __init__(self, parent, controller, key=None):
        # Initialize frame
        super().__init__(parent, controller, key)

    def _init_variables(self):
        # Call parent method
        super(YAxisDataSet, self)._init_variables()

        # Instantiate observable variables
        self.legend_txt = tk.StringVar(value="y data name")
        self.is_legend = tk.BooleanVar(value=False)
        self.is_plotted = tk.BooleanVar(value=False)

    def _create_widgets(self):
        # Call parent method
        super(YAxisDataSet, self)._create_widgets()

        # Instantiate nested widgets
        self.legend_lbl = ttk.Label(master=self, text='    Include legend:')
        self.legend_chkbtn = ttk.Checkbutton(self, onvalue=True, text="",
                                             variable=self.is_legend)
        self.legend_entry = ttk.Entry(master=self, width=15,
                                      textvariable=self.legend_txt)
        self.plot_lbl = ttk.Label(master=self, text='    Show line:')
        self.plot_chkbtn = ttk.Checkbutton(self, onvalue=True, text="",
                                             variable=self.is_plotted)
        self.plot_btn = BlueButton(master=self, text="Redraw plot",
                                   command=self.edit_data_set)
        self.destroy_btn = BlueButton(master=self, text="Remove plot",
                                      command=self.destroy_data_set)

    def _position_widgets(self):
        # Call parent method
        super(YAxisDataSet, self)._position_widgets()

        # Position nested widgets
        self.legend_lbl.grid(row=0, column=8)
        self.legend_chkbtn.grid(row=0, column=9)
        self.legend_entry.grid(row=0, column=10)
        self.plot_lbl.grid(row=0, column=11)
        self.plot_chkbtn.grid(row=0, column=12)
        self.plot_btn.grid(row=0, column=13, padx=2)
        self.destroy_btn.grid(row=0, column=14, padx=2)

    def edit_data_set(self):
        self.c.edit_data_set(self.key)

    def destroy_data_set(self):
        self.c.remove_data_set(self.key)
        self.destroy()
