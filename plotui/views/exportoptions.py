import views.styles as st


class ExportOptionsFrame(st.SubFrame):
    """
    The visual design for the Plot element.
    """
    def _create_widgets(self):
        self._title_lbl = st.TitleLabel(self, "Export Options")
        self._export_lbl = st.Label(self, "Export type:")
        self._export_rdb = st.Radiobuttons(self, ["PNG image", "LaTeX data"])
        self._file_le = st.StringLabEnt(self, "File name:", "graph")
        self._export_btn = st.Button(self, "Export", self.export)

    def _position_widgets(self):
        self._title_lbl.grid(row=0)
        self._export_lbl.grid(row=1, sticky='w')
        self._export_rdb.grid(row=2, sticky='w')
        self._file_le.grid(row=3, sticky='w')
        self._export_btn.grid(row=4, sticky='w')

    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=1)

    def export(self):
        self._c.export(self._export_rdb.get_index(), self._file_le.get())
