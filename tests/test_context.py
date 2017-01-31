# -*- coding: utf-8 -*-

import pytest

from entitas import Context, Entity, MissingEntity


def test_create_context():
    context = Context()
    assert context._entity_index == 0
    assert context.count == 0

def test_create_entity():
    context = Context()
    entity = context.create_entity()
    assert context.count == 1
    assert context.has(entity)
    assert isinstance(entity, Entity)

def test_destroy_entity():
    context = Context()
    entity = context.create_entity()
    context.destroy(entity)
    assert not context.has(entity)
    with pytest.raises(MissingEntity):
        context.destroy(entity)
