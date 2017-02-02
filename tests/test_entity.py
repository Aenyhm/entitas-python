# -*- coding: utf-8 -*-

from collections import namedtuple

import pytest

from entitas import Entity, AlreadyAddedComponent, MissingComponent


Movable = namedtuple('Movable', [])
Health = namedtuple('Health', ['value'])
Position = namedtuple('Position', ['x', 'y'])


def test_create_entity():
    entity = Entity()
    assert entity.creation_index == 0
    assert entity.count == 0
    assert not entity.has_any(Movable, Position)


def test_add_comp_a():
    entity = Entity()
    entity.add(Movable)
    assert entity.count == 1
    assert entity.has(Movable)
    assert not entity.has(Position)
    assert isinstance(entity.get(Movable), Movable)
    with pytest.raises(MissingComponent):
        entity.get(Position)


def test_add_two_comp_a():
    entity = Entity()
    entity.add(Movable)
    with pytest.raises(AlreadyAddedComponent):
        entity.add(Movable)


def test_remove_comp_a():
    entity = Entity()
    entity.add(Movable)
    entity.remove(Movable)
    assert not entity.has(Movable)
    assert entity.count == 0
    with pytest.raises(MissingComponent):
        entity.remove(Movable)


def test_add_comp_b():
    entity = Entity()
    entity.add(Position, 1, 2)
    assert entity.get(Position).x == 1
    assert entity.get(Position).y == 2


def test_replace_comp_b():
    entity = Entity()
    entity.add(Position, 1, 2)
    entity.replace(Position, 3, 4)
    assert entity.count == 1
    assert entity.get(Position).x == 3
    assert entity.get(Position).y == 4


def test_destroy_entity():
    entity = Entity()
    entity.add(Movable)
    entity.add(Position, 1, 2)
    assert entity.count == 2
    assert entity.has(Movable, Position)
    entity.destroy()
    assert entity.count == 0


def test_readme_example():
    entity = Entity()
    entity.add(Position, 3, 7)
    entity.add(Health, 100)
    entity.add(Movable)
    entity.replace(Position, 10, 100)
    entity.replace(Health, entity.get(Health).value - 1)
    entity.remove(Position)
    has_pos = entity.has(Position)
    movable = entity.has(Movable)
    assert not has_pos
    assert movable
    assert entity.get(Health).value == 99
