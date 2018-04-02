import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from controllers import Controller


class View(tk.Tk):
    """
    The root level element.
    """
    def __init__(self):
        # Initialise the base level element
        tk.Tk.__init__(self)
        self.controller = Controller(self)

        # Instantiate nested widgets
        self.plot = PlotFrame(self, self.controller)
        self.graph_options = GraphOptionsFrame(self, self.controller)
        self.plot_options = PlotOptionsFrame(self, self.controller)

        # Position nested widgets
        self.plot.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.graph_options.grid(row=0, column=0)
        self.plot_options.grid(row=1, column=0)

        # Configure base grid layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Once widgets are instantiated bind events

        # Enter the event loop
        self.mainloop()

    def redraw_canvas(self):
        self.plot.canvas.draw()


class PlotFrame(ttk.Frame):
    """
    The visual design for the Plot element.
    """
    def __init__(self, parent, controller, **kwargs):
        # Initialize frame
        self.controller = controller
        ttk.Frame.__init__(self, parent, **kwargs)

        # Instantiate nested widgets
        self.canvas = FigureCanvasTkAgg(
            self.controller.get_plot_figure(),
            self,
        )
        self.plot = self.canvas.get_tk_widget()

        # Position nested widgets
        self.plot.grid()


class GraphOptionsFrame(ttk.Frame):
    """
    The visual design for the Plot element.
    """
    def __init__(self, parent, controller, **kwargs):
        # Initialize frame
        self.c = controller
        ttk.Frame.__init__(self, parent, **kwargs)

        # Instantiate observable variables
        self.title_txt = tk.StringVar()
        self.xlabel_txt = tk.StringVar()
        self.ylabel_txt = tk.StringVar()

        # Instantiate nested widgets
        title_label = ttk.Label(self, text="Graph Options")
        # Buttons
        title_btn = ttk.Button(
            self, text="Add title",
            command=lambda: self.c.set_title(self.title_txt.get()),
            )
        x_axis_btn = ttk.Button(
            self, text="Add x-axis label",
            command=lambda: self.c.set_xlabel(self.xlabel_txt.get()),
            )
        y_axis_btn = ttk.Button(
            self, text="Add y-axis label",
            command=lambda: self.c.set_ylabel(self.ylabel_txt.get()),
            )
        # Entrys
        title_entry = ttk.Entry(self, textvariable=self.title_txt)
        x_axis_entry = ttk.Entry(self, textvariable=self.xlabel_txt)
        y_axis_entry = ttk.Entry(self, textvariable=self.ylabel_txt)

        # Position nested widgets
        title_label.grid(row=0, column=0, columnspan=2)
        title_btn.grid(row=1, column=0)
        x_axis_btn.grid(row=2, column=0)
        y_axis_btn.grid(row=3, column=0)
        title_entry.grid(row=1, column=1)
        x_axis_entry.grid(row=2, column=1)
        y_axis_entry.grid(row=3, column=1)


class PlotOptionsFrame(ttk.Frame):
    """
    The visual design for the Plot element.
    """
    def __init__(self, parent, controller, **kwargs):
        # Initialize frame
        self.controller = controller
        ttk.Frame.__init__(self, parent, **kwargs)

        # Instantiate nested widgets
        self.title_label = ttk.Label(self, text="Plot Options")
        self.button1 = ttk.Button(
            self, text="Add Plot", command=self.plot_model_line,
        )
        self.button2 = ttk.Button(
            self, text="Remove Plot", command=self.remove_line,
        )

        # Position nested widgets
        self.title_label.grid(row=0, column=0)
        self.button1.grid(row=0, column=0)
        self.button2.grid(row=1, column=0)

    def plot_model_line(self):
        self.controller.plot_model_line()

    def remove_line(self):
        self.controller.remove_line()
