# -*- coding: utf-8 -*-

from .utils import has_method


class Processors():

    def __init__(self):
        self._execute_systems = []

    def add(self, system):
        if has_method(system, 'execute'):
            self._execute_systems.append(system)

    def execute(self):
        for system in self._execute_systems:
            system.execute()
