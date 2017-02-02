# -*- coding: utf-8 -*-


def get_expr_repr(expr):
    return '' if expr is None else ','.join([x.__name__ for x in expr])


class Matcher(object):

    def __init__(self, all_of=None, any_of=None, none_of=None):
        self._all = all_of
        self._any = any_of
        self._none = none_of

    def matches(self, entity):
        all_cond = self._all is None or entity.has(*self._all)
        any_cond = self._any is None or entity.has_any(*self._any)
        none_cond = self._none is None or not entity.has_any(*self._none)

        return all_cond and any_cond and none_cond

    def __repr__(self):
        return '<Matcher [all=({}) any=({}) none=({})]>'.format(
            get_expr_repr(self._all),
            get_expr_repr(self._any),
            get_expr_repr(self._none))
