import tkinter as tk
from tkinter import ttk

from views.styles import BlueButton


class GraphOptionsFrame(ttk.Frame):
    """
    The visual design for the Plot element.
    """
    def __init__(self, parent, controller):
        # Initialize frame
        ttk.Frame.__init__(self, parent, style='Sub.TFrame', border=5)
        self.c = controller

        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self):
        # Instantiate nested widgets
        self.main_title_lbl = ttk.Label(self, text="Graph Options",
                                style='Title.TLabel')
        self.graph_label_options = GraphLabelOptionsFrame(self, self.c)
        self.graph_scaling_options = GraphScalingOptionsFrame(self, self.c)

    def _position_widgets(self):
        # Position nested widgets
        self.main_title_lbl.grid(row=0, column=0, columnspan=1)
        self.graph_label_options.grid(row=1, column=0, sticky="we")
        self.graph_scaling_options.grid(row=2, column=0, sticky="we")

        # Configure rows and columns
        self.grid_columnconfigure(0, pad=5)


class GraphLabelOptionsFrame(ttk.Frame):
    """
    The frame containing customisation options for graph text labels.
    """
    def __init__(self, parent, controller):
        # Initialize frame
        ttk.Frame.__init__(self, parent)
        self.c = controller

        # Instantiate observable variables
        self.title_txt = tk.StringVar()
        self.xlabel_txt = tk.StringVar()
        self.ylabel_txt = tk.StringVar()

        # Create and position widgets
        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self):
        # Instantiate nested widgets
        self.main_title_lbl = ttk.Label(self, text="Label options",
                                style='SubTitle.TLabel')

        # Buttons
        self.title_btn = BlueButton(
            master=self, text="Add title",
            command=lambda: self.c.set_title(self.title_txt.get()),
            )
        self.x_label_btn = BlueButton(
            master=self, text="Add x-axis label",
            command=lambda: self.c.set_xlabel(self.xlabel_txt.get()),
            )
        self.y_label_btn = BlueButton(
            master=self, text="Add y-axis label",
            command=lambda: self.c.set_ylabel(self.ylabel_txt.get()),
            )

        # Entrys
        self.title_entry = ttk.Entry(self, textvariable=self.title_txt)
        self.x_label_entry = ttk.Entry(self, textvariable=self.xlabel_txt)
        self.y_label_entry = ttk.Entry(self, textvariable=self.ylabel_txt)

    def _position_widgets(self):
        # Position nested widgets
        self.main_title_lbl.grid(row=1, column=0, columnspan=2, sticky='w')

        self.title_btn.grid(row=2, column=0, sticky="w")
        self.x_label_btn.grid(row=3, column=0, sticky="w")
        self.y_label_btn.grid(row=4, column=0, sticky="w")

        self.title_entry.grid(row=2, column=1, sticky="w")
        self.x_label_entry.grid(row=3, column=1, sticky="w")
        self.y_label_entry.grid(row=4, column=1, sticky="w")

        # Configure rows and columns
        self.grid_columnconfigure(0, pad=5)
        # TODO pad the buttons


class GraphScalingOptionsFrame(ttk.Frame):
    """
    The frame containing customisation options for graph text labels.
    """
    def __init__(self, parent, controller):
        # Initialize frame
        ttk.Frame.__init__(self, parent)
        self.c = controller

        # Instantiate observable variables
        self.xmin_txt = tk.StringVar()
        self.xmax_txt = tk.StringVar()
        self.ymin_txt = tk.StringVar()
        self.ymax_txt = tk.StringVar()

        # Create and position widgets
        self._create_widgets()
        self._position_widgets()

    def _create_widgets(self):
        # Instantiate nested widgets
        self.main_title_lbl = ttk.Label(self, text="Scaling options",
                                style='SubTitle.TLabel')

        self.xmin_lbl = ttk.Label(master=self, text='X-axis min')
        self.xmax_lbl = ttk.Label(master=self, text='X-axis max')
        self.ymin_lbl = ttk.Label(master=self, text='Y-axis min')
        self.ymax_lbl = ttk.Label(master=self, text='Y-axis max')

        self.xmin_entry = ttk.Entry(master=self, width=10,
                                    textvariable=self.xmin_txt)
        self.xmax_entry = ttk.Entry(master=self, width=10,
                                    textvariable=self.xmax_txt)
        self.ymin_entry = ttk.Entry(master=self, width=10,
                                    textvariable=self.ymin_txt)
        self.ymax_entry = ttk.Entry(master=self, width=10,
                                    textvariable=self.ymax_txt)

    def _position_widgets(self):
        # Position nested widgets
        self.main_title_lbl.grid(row=0, column=0, columnspan=4, sticky='w')

        # Labels
        self.xmin_lbl.grid(row=1, column=0, sticky='w')
        self.xmax_lbl.grid(row=1, column=2, sticky='w')
        self.ymin_lbl.grid(row=2, column=0, sticky='w')
        self.ymax_lbl.grid(row=2, column=2, sticky='w')

        # Entrys
        self.xmin_entry.grid(row=1, column=1, sticky='w')
        self.xmax_entry.grid(row=1, column=3, sticky='w')
        self.ymin_entry.grid(row=2, column=1, sticky='w')
        self.ymax_entry.grid(row=2, column=3, sticky='w')

