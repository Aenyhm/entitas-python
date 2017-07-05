import pytest
from entitas import Entity, AlreadyAddedComponent, MissingComponent
from .test_components import Movable, Position

_entity = Entity()


class TestEntity(object):

    def test_entry_points(self):
        Entity.activate
        Entity.add
        Entity.remove
        Entity.replace
        Entity.get
        Entity.has
        Entity.has_any
        Entity.remove_all
        Entity.destroy

    def test_has(self):
        _entity.activate(0)
        _entity.add(Movable)
        assert _entity.has(Movable)
        assert isinstance(_entity.get(Movable), Movable)
        assert not _entity.has(Position)

    def test_has_any(self):
        assert _entity.has_any(Movable, Position)

    def test_add(self):
        with pytest.raises(MissingComponent):
            _entity.get(Position)

        with pytest.raises(AlreadyAddedComponent):
            _entity.add(Movable)

        _entity.add(Position, 1, 2)
        assert _entity.get(Position).x == 1
        assert _entity.get(Position).y == 2

    def test_replace(self):
        _entity.replace(Position, 3, 4)
        assert _entity.get(Position).x == 3
        assert _entity.get(Position).y == 4

    def test_remove(self):
        _entity.remove(Movable)
        assert not _entity.has(Movable)
        with pytest.raises(MissingComponent):
            _entity.remove(Movable)

    def test_destroy(self):
        _entity.destroy()
        assert not _entity.has(Movable, Position)
