class Event(object):
    """C# events in Python."""

    def __init__(self):
        self._listeners = []

    def __call__(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)

    def __add__(self, listener):
        if listener not in self._listeners:
            self._listeners.append(listener)
        return self

    def __sub__(self, listener):
        if listener in self._listeners:
            self._listeners.remove(listener)
        return self
