# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from .collector import Collector


class ExecuteProcessor(metaclass=ABCMeta):

    @abstractmethod
    def execute(self):
        pass


class ReactiveProcessor(ExecuteProcessor):

    def __init__(self, context):
        self._collector = self._get_collector(context)
        self._buffer = []

    @abstractmethod
    def get_trigger(self):
        pass

    @abstractmethod
    def filter(self, entity):
        pass

    @abstractmethod
    def react(self, entities):
        pass

    def activate(self):
        self._collector.activate()

    def deactivate(self):
        self._collector.deactivate()

    def clear(self):
        self._collector.clear_collected_entities()

    def execute(self):
        if len(self._collector.collected_entities) != 0:
            for entity in self._collector.collected_entities:
                if self.filter(entity):
                    self._buffer.append(entity)

            self._collector.clear_collected_entities()

            if len(self._buffer) != 0:
                self.react(self._buffer)
                self._buffer.clear()

    def _get_collector(self, context):
        trigger = self.get_trigger()
        collector = Collector()

        for matcher in trigger:
            group_event = trigger[matcher]
            group = context.get_group(matcher)
            collector.add(group, group_event)

        print(collector)

        return collector


class Processors():

    def __init__(self):
        self._execute_processors = []

    def add(self, processor):
        if isinstance(processor, ExecuteProcessor):
            self._execute_processors.append(processor)

    def execute(self):
        for processor in self._execute_processors:
            processor.execute()

    def activate_reactive_processors(self):
        for processor in self._execute_processors:
            if isinstance(processor, ReactiveProcessor):
                print('ReactiveProcessor', processor)
                processor.activate()

    def deactivate_reactive_processors(self):
        for processor in self._execute_processors:
            if issubclass(processor, ReactiveProcessor):
                processor.deactivate()

    def clear_reactive_processors(self):
        for processor in self._execute_processors:
            if issubclass(processor, ReactiveProcessor):
                processor.clear()
