# -*- coding: utf-8 -*-


class EntitasException(Exception):
    pass


class ExistingComponentException(EntitasException):
    pass


class MissingComponentException(EntitasException):
    pass
