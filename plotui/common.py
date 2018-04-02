class Observable(object):
    """
    A class which allows subscribers to fire events when changing a
    variable's value. Storing callbacks as a dictionary instead of a
    list means that the same function cannot be added multiple times.
    """
    def __init__(self, initial_value=None):
        self.data = initial_value
        self.callbacks = {}

    def add_callback(self, func):
        self.callbacks[func] = 1

    def del_callback(self, func):
        del self.callbacks[func]

    def _do_callbacks(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data):
        self.data = data
        self._do_callbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None


class ObservableList(object):
    """
    A class which allows subscribers to fire events when changing a
    variable's value. Storing callbacks as a dictionary instead of a
    list means that the same function cannot be added multiple times.
    """
    def __init__(self, initial_value=None):
        self.data = [initial_value]
        self.callbacks = {}

    def add_callback(self, func):
        self.callbacks[func] = 1

    def del_callback(self, func):
        del self.callbacks[func]

    def _do_callbacks(self, data):
        for func in self.callbacks:
            func(data)

    def append(self, data):
        self.data.append(data)
        self._do_callbacks(data)

    def remove(self, data):
        self.data.remove(data)
        self._do_callbacks(data)

    def unset(self):
        self.data = None

    def len(self):
        return len(self.data)
