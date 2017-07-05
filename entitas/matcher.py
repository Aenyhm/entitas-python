def get_expr_repr(expr):
    return '' if expr is None else ','.join([x.__name__ for x in expr])


class Matcher(object):

    def __init__(self, *args, **kwargs):
        self._all = args if args else kwargs.get('all_of', None)
        self._any = kwargs.get('any_of', None)
        self._none = kwargs.get('none_of', None)

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
