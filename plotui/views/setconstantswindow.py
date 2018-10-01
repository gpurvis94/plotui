import tkinter as tk

import views.styles as st


class SetConstantsWindow(tk.Toplevel):
    def __init__(self, parent, controller, key, plot_type):
        tk.Toplevel.__init__(self, parent)
        self._frame = MainFrame(self, controller, key, plot_type)
        self._frame.grid()


class MainFrame(st.MainFrame):
    def __init__(self, parent, controller, key, plot_type):
        self._key = key
        self._type = plot_type
        super().__init__(parent, controller)

    def _create_widgets(self):
        self._constants_frame = ConstantsFrame(self, self._c, self._key,
            self._type)
        self._actions_frame = ActionsFrame(self, self._c)

    def _position_widgets(self):
        self._constants_frame.grid(row=0, column=0, sticky="nsew")
        self._actions_frame.grid(row=1, column=0, sticky="nsew")

    def _configure_grid(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def save(self):
        self._c.save_entry_vals(self._key,
            self._constants_frame.get_entry_vals())

    def destroy_window(self):
        self._parent.destroy()


class ConstantsFrame(st.SubSubFrame):
    def __init__(self, parent, controller, key, plot_type):
        self._key = key
        self._type = plot_type
        super().__init__(parent, controller)

    def _init_variables(self):
        self.constants = self._c.get_constant_strings(self._type)
        self.initial_vals = self._c.get_constant_vals(self._key)

    def _create_widgets(self):
        self.label = st.SubTitleLabel(self, "Constants")
        self.const_les = []

    def _position_widgets(self):
        self.label.grid(row=0, column=0, sticky='w')

    def _create_optional_widgets(self):
        for constant, initial_val in zip(self.constants, self.initial_vals):
            const_le = st.FloatLabEnt(self, f"{constant}:",initial_val)
            const_le.grid(sticky='w')
            self.const_les.append(const_le)

    def get_entry_vals(self):
        const_vals = []
        for const_le in self.const_les:
            const_vals.append(const_le.get())
        return const_vals


class ActionsFrame(st.SubSubFrame):
    def _init_variables(self):
        pass

    def _create_widgets(self):
        self.save_and_close_btn = st.Button(self, "Save and close",
            self.save_and_close)
        self.close_btn = st.Button(self, "Close", self.close)

    def _position_widgets(self):
        self.save_and_close_btn.grid(row=0, column=0)
        self.close_btn.grid(row=0, column=1)

    def save_and_close(self):
        self._parent.save()
        self._parent.destroy_window()

    def close(self):
        self._parent.destroy_window()
