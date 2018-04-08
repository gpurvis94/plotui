import tkinter as tk
from tkinter import ttk

from views.styles import SubFrame, SubSubFrame, BlueButton


class ExportOptionsFrame(SubFrame):
    """
    The visual design for the Plot element.
    """
    def _init_variables(self):
        self._file_name_txt = tk.StringVar(value="graph")

    def _create_widgets(self):
        # Instantiate nested widgets
        self._main_title_lbl = ttk.Label(self, text="Export Options",
            style='Title.TLabel')
        self._export_types_lbl = ttk.Label(self, text="Export type:")
        self._export_types_rdb = ExportTypesFrame(self, self._c)
        self._file_name_lbl = ttk.Label(self, text="File name:")
        self._file_name_entry = ttk.Entry(self, width=15,
            textvariable=self._file_name_txt)
        self._export_btn = BlueButton(self, text="Export",
            command=self._export)

    def _position_widgets(self):
        # Position nested widgets
        self._main_title_lbl.grid(row=0, column=0, columnspan=2)
        self._export_types_lbl.grid(row=1, column=0, columnspan=2, sticky='w')
        self._export_types_rdb.grid(row=2, column=0, columnspan=2, sticky='w')
        self._file_name_lbl.grid(row=3, column=0, sticky='w')
        self._file_name_entry.grid(row=3, column=1, sticky='w')
        self._export_btn.grid(row=4, column=0, columnspan=2, sticky='w',
            pady=2)

        self.grid_columnconfigure(0, weight=0, pad=5)
        self.grid_columnconfigure(1, weight=1, pad=5)

    ####################################################################
    #                          Exporting data                          #
    ####################################################################

    def _export(self):
        self._c.export(self._export_types_rdb.selected_index.get(),
            self._file_name_txt.get())


class ExportTypesFrame(SubSubFrame):
    """
    The radiobutton selections for export types.
    """
    def _init_variables(self):
        self._export_types = [
            "PNG image",
            "LaTeX dat file",
            ]
        self.selected_index = tk.IntVar(value=0)

    def _create_widgets(self):
        for count, export_type in enumerate(self._export_types):
            ttk.Radiobutton(self, text=export_type,
                variable=self.selected_index, value=count).grid(
                    sticky='w', padx=5)


