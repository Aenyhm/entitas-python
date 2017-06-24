# -*- coding: utf-8 -*-

import pytest

from entitas import Context, Entity, MissingEntity


_context = Context()
_entity = _context.create_entity()


class TestContext(object):

    def test_entry_points(self):
        Context.create_entity
        Context.has_entity
        Context.destroy_entity
        Context.entities

        Context.get_group

        Context.set_unique_component
        Context.get_unique_component

    def test_has_entity(self):
        assert _context.has_entity(_entity)
        assert isinstance(_entity, Entity)

    def test_entities(self):
        assert len(_context.entities) == 1

    def test_destroy_entity(self):
        _context.destroy_entity(_entity)
        assert not _context.has_entity(_entity)

        with pytest.raises(MissingEntity):
            _context.destroy_entity(_entity)
