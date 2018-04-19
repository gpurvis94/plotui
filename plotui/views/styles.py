import tkinter as tk
from tkinter import ttk


########################################################################
#                                Frames                                #
########################################################################

class BaseFrame(ttk.Frame):
    """
    The base class for all custom frames. When initializing a custom
    frame, instead of using __init__(), override the methods below.
    """
    def __init__(self, parent, controller, style='TFrame', border=0):
        ttk.Frame.__init__(self, parent, style=style, border=border)
        self._c = controller
        self._parent = parent

        self._init_variables()
        self._create_widgets()
        self._position_widgets()
        self._create_optional_widgets()
        self._pad_columns()
        self._pad_rows()
        self._configure_grid()

    def _init_variables(self):
        pass

    def _create_widgets(self):
        pass

    def _position_widgets(self):
        pass

    def _create_optional_widgets(self):
        pass

    def _pad_columns(self, padding=5):
        for col_i in range(self.grid_size()[0]):
            self.grid_columnconfigure(col_i, pad=padding)

    def _pad_rows(self, padding=2):
        for row_i in range(self.grid_size()[1]):
            self.grid_rowconfigure(row_i, pad=padding)

    def _configure_grid(self):
        pass


class MainFrame(BaseFrame):
    """
    A frame defining the properties of the main window frame.
    """
    def __init__(self, parent, controller, style='Main.TFrame', border=5):
        super().__init__(parent, controller, style, border)


class SubFrame(BaseFrame):
    """
    A frame defining the properties of a frame within the main window.
    """
    def __init__(self, parent, controller, style='Sub.TFrame', border=5):
        super().__init__(parent, controller, style, border)


class SubSubFrame(BaseFrame):
    """
    A frame defining the properties of a frame within a SubFrame.
    """
    def __init__(self, parent, controller, style='TFrame', border=0):
        super().__init__(parent, controller, style, border)


########################################################################
#                                Labels                                #
########################################################################

class TitleLabel(ttk.Label):
    """
    A label defining the properties of an entry for labels.
    """
    def __init__(self, parent, text, style='Title.TLabel'):
        ttk.Label.__init__(self, parent, text=text, style=style)

class SubTitleLabel(ttk.Label):
    """
    A label defining the properties of an entry for labels.
    """
    def __init__(self, parent, text, style='SubTitle.TLabel'):
        ttk.Label.__init__(self, parent, text=text, style=style)

class Label(ttk.Label):
    """
    A label defining the properties of an entry for labels.
    """
    def __init__(self, parent, text, style='TLabel'):
        ttk.Label.__init__(self, parent, text=text, style=style)

########################################################################
#                                Entrys                                #
########################################################################

class BaseObservableEntry(ttk.Entry):
    """
    An entry that automatically creates its own observable values.
    """
    def __init__(self, parent, ObservableClass, initial_value, width, style):
        self._observable_var = ObservableClass(value=initial_value)
        ttk.Entry.__init__(self, parent, width=width, style=style,
            textvariable=self._observable_var)

    def get(self):
        return self._observable_var.get()

    def set(self, value):
        self._observable_var.set(value)

class FloatEntry(BaseObservableEntry):
    """
    An entry defining the properties of an entry for numbers.
    """
    def __init__(self, parent, initial_var, width=8, style='Number.TEntry'):
        super().__init__(parent, tk.DoubleVar, initial_var, width, style)

class StringEntry(BaseObservableEntry):
    """
    An entry defining the properties of an entry for strings.
    """
    def __init__(self, parent, initial_var, width=16, style='String.TEntry'):
        super().__init__(parent, tk.StringVar, initial_var, width, style)


########################################################################
#                           Labelled Entrys                            #
########################################################################

class BaseObservableLabEnt(ttk.Frame):
    """
    A frame defining the properties of an observable labelled entry.
    """
    def __init__(self, parent, text, initial_var, EntryClass):
        ttk.Frame.__init__(self, parent, style='TFrame')
        self.label = Label(self, text)
        self.entry = EntryClass(self, initial_var)
        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.set(value)

class FloatLabEnt(BaseObservableLabEnt):
    """
    Defines the properties of an observable labelled entry for numbers.
    """
    def __init__(self, parent, text, initial_var):
        super().__init__(parent, text, initial_var, FloatEntry)

class StringLabEnt(BaseObservableLabEnt):
    """
    Defines the properties of an observable labelled entry for strings.
    """
    def __init__(self, parent, text, initial_var):
        super().__init__(parent, text, initial_var, StringEntry)

########################################################################
#                          Checkbutton Entrys                          #
########################################################################

class BaseObservableChkEnt(ttk.Frame):
    """
    A frame defining the properties of an entry with a checkbox.
    """
    def __init__(self, parent, text, initial_var, EntryClass):
        ttk.Frame.__init__(self, parent, style='TFrame')
        self.check = BoolCheck(self, text)
        self.entry = EntryClass(self, initial_var)
        self.check.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)

    def get_check(self):
        return self.check.get()

    def get_entry(self):
        return self.entry.get()


class StringChkEnt(BaseObservableChkEnt):
    """
    Defines the properties of an observable check entry for strings.
    """
    def __init__(self, parent, text, initial_var):
        super().__init__(parent, text, initial_var, StringEntry)


########################################################################
#                               Buttons                                #
########################################################################

class Button(tk.Button):
    """
    Defines the looks of the standard button
    """
    def __init__(self, master, text, command=None):
        super().__init__(master=master, text=text, command=command,
            font="Helvetica 8 bold", bg='#1874CD', fg='white',
            activebackground='#104E8B', bd=2, highlightthickness=0)


########################################################################
#                             Checkbuttons                             #
########################################################################

class BoolCheck(ttk.Checkbutton):
    """
    An entry that automatically creates its own observable values.
    """
    def __init__(self, parent, text, value=False, style='TCheckbutton'):
        self._observable_var = tk.BooleanVar(value=value)
        ttk.Checkbutton.__init__(self, parent, text=text, style=style,
            variable=self._observable_var)

    def get(self):
        return self._observable_var.get()

    def set(self, value):
        self._observable_var.set(value)


########################################################################
#                              Comboboxes                              #
########################################################################

class BaseObservableCombobox(ttk.Combobox):
    """
    An entry that automatically creates its own observable values.
    """
    def __init__(self, parent, ObservableClass, values, width, style):
        self._observable_var = ObservableClass(value=values[0])
        ttk.Combobox.__init__(self, parent, width=width, style=style,
            textvariable=self._observable_var, values=values)

    def get(self):
        return self._observable_var.get()

class StringCombo(BaseObservableCombobox):
    def __init__(self, parent, values, width=12, style='TCombobox'):
        super().__init__(parent, tk.StringVar, values, width, style)


########################################################################
#                             Radiobuttons                             #
########################################################################

class Radiobuttons(ttk.Frame):
    """
    A frame defining the appearance of a series of radiobuttons.
    """
    def __init__(self, parent, values):
        ttk.Frame.__init__(self, parent, style='TFrame')
        self._values = values
        self._index = tk.IntVar(value=0)

        for count, val in enumerate(values):
            ttk.Radiobutton(self, text=val, value=count,
                variable=self._index).grid()

    def get_index(self):
        return self._index.get()

    def get_value(self):
        return self._values[self._index.get()]
