import tkinter as tk

import views.styles as st


class GraphOptionsFrame(st.SubFrame):
    """
    The visual design for the graph options frame.
    """
    def _create_widgets(self):
        self._title_lbl = st.TitleLabel(self, "Graph Options")
        self._graph_label_options = GraphLabelOptionsFrame(self, self._c)
        self._graph_scaling_options = GraphScalingOptionsFrame(self, self._c)
        self._graph_tick_mark_options = GraphTickMarkOptions(self, self._c)

    def _position_widgets(self):
        self._title_lbl.grid(row=0)
        self._graph_label_options.grid(row=1, sticky="we")
        self._graph_scaling_options.grid(row=2, sticky="we")
        self._graph_tick_mark_options.grid(row=3, sticky="we")

    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=1)


class GraphLabelOptionsFrame(st.SubSubFrame):
    """
    The frame containing customisation options for the artist labels.
    """
    def _create_widgets(self):
        self._title_lbl = st.SubTitleLabel(self, "Label options")
        self._title_btn = st.Button(self, "Add title", self.set_title)
        self._xlabel_btn = st.Button(self, "Add x-axis label", self.set_xlabel)
        self._ylabel_btn = st.Button(self, "Add y-axis label", self.set_ylabel)
        self._title_entry = st.StringEntry(self, "Title")
        self._xlabel_entry = st.StringEntry(self, "x axis")
        self._ylabel_entry = st.StringEntry(self, "y axis")

    def _position_widgets(self):
        self._title_lbl.grid(row=1, column=0, columnspan=2, sticky='w')
        self._title_btn.grid(row=2, column=0, sticky="w")
        self._xlabel_btn.grid(row=3, column=0, sticky="w")
        self._ylabel_btn.grid(row=4, column=0, sticky="w")
        self._title_entry.grid(row=2, column=1, sticky="w")
        self._xlabel_entry.grid(row=3, column=1, sticky="w")
        self._ylabel_entry.grid(row=4, column=1, sticky="w")

    def set_title(self):
        self._c.set_title(self._title_entry.get())

    def set_xlabel(self):
        self._c.set_xlabel(self._xlabel_entry.get())

    def set_ylabel(self):
        self._c.set_ylabel(self._ylabel_entry.get())


class GraphScalingOptionsFrame(st.SubSubFrame):
    """
    The frame containing customisation options for graph text labels.
    """
    def _create_widgets(self):
        self._title_lbl = st.SubTitleLabel(self, "Scaling options")
        self._xmin_le = st.FloatLabEnt(self, "X-axis min:", 0.0)
        self._xmax_le = st.FloatLabEnt(self, 'X-axis max:', 1.0)
        self._ymin_le = st.FloatLabEnt(self, 'Y-axis min:', 0.0)
        self._ymax_le = st.FloatLabEnt(self, 'Y-axis max:', 1.0)
        self._scale_btn = st.Button(self, "Scale", self.scale)
        self._autoscale_btn = st.Button(self, "Autoscale", self.autoscale)

    def _position_widgets(self):
        self._title_lbl.grid(row=0, column=0, columnspan=4, sticky='w')
        self._xmin_le.grid(row=1, column=0, sticky='w')
        self._xmax_le.grid(row=1, column=1, sticky='w')
        self._ymin_le.grid(row=2, column=0, sticky='w')
        self._ymax_le.grid(row=2, column=1, sticky='w')
        self._scale_btn.grid(row=3, column=0)
        self._autoscale_btn.grid(row=3, column=1)

    def scale(self):
        try:
            self._c.scale_axis(self._xmin_le.get(), self._xmax_le.get(),
                self._ymin_le.get(), self._ymax_le.get())
        except tk.TclError:
            self._c.message("Error", "Scale value must be a number.")

    def autoscale(self):
        tup = self._c.autoscale_axis()
        if tup is None:
            return
        self._xmin_le.set(tup[0])
        self._xmax_le.set(tup[1])
        self._ymin_le.set(tup[2])
        self._ymax_le.set(tup[3])


class GraphTickMarkOptions(st.SubSubFrame):
    """
    The frame containing customisation options for graph text labels.
    """
    def _create_widgets(self):
        self._title_lbl = st.SubTitleLabel(self, "Tick mark options")

    def _position_widgets(self):
        self._title_lbl.grid(row=0, column=0, sticky='w')
