# -*- coding: utf-8 -*-

from collections import namedtuple

import pytest

from entitas import Context, Entity, Matcher, MissingEntity


CompA = namedtuple('CompA', [])
CompB = namedtuple('CompB', [])
CompC = namedtuple('CompC', [])
CompD = namedtuple('CompD', [])
CompE = namedtuple('CompE', [])
CompF = namedtuple('CompF', [])
Movable = namedtuple('Movable', [])
Position = namedtuple('Position', ['x', 'y'])


def test_create_context():
    context = Context()
    assert context._entity_index == 0
    assert context.count == 0


def test_create_entity():
    context = Context()
    entity = context.create_entity()
    assert context.count == 1
    assert context.has_entity(entity)
    assert isinstance(entity, Entity)


def test_destroy_entity():
    context = Context()
    entity = context.create_entity()
    context.destroy_entity(entity)
    assert not context.has_entity(entity)
    with pytest.raises(MissingEntity):
        context.destroy_entity(entity)


def test_readme_example():
    context = Context()
    entity = context.create_entity()
    entity.add(Movable)
    entity.add(Position, 3, 7)

    entities = context.entities
    assert len(entities) == 1

    for e in entities:
        assert e.has(Movable, Position)
