from entitas import Context, Matcher
from .test_components import Movable

_context = Context()
_entity = _context.create_entity()
_entity.add(Movable)
_group = _context.get_group(Matcher(Movable))


class TestGroup(object):

    def test_entities(self):
        assert len(_group.entities) == 1

    def test_single_entity(self):
        assert _group.single_entity.has(Movable)

    def test_events(self):
        assert _group.single_entity == _entity
        _entity.replace(Movable)
        assert _group.single_entity == _entity
        _entity.remove(Movable)
        assert not _group.single_entity
