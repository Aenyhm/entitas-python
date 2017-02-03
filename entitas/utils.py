# -*- coding: utf-8 -*-


class Event(object):
    """ C# events in Python. """

    def __init__(self):
        self.listeners = []

    def __call__(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)

    def __add__(self, listener):
        self.listeners.append(listener)
        return self

    def __sub__(self, listener):
        self.listeners.remove(listener)
        return self
