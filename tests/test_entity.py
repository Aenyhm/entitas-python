# -*- coding: utf-8 -*-

import pytest

from collections import namedtuple
from entitas import Entity, AlreadyAddedComponent, MissingComponent


CompA = namedtuple('CompA', [])
CompB = namedtuple('CompB', ['x', 'y', 'z'])


def test_create_entity():
    entity = Entity()
    assert entity.creation_index == 0
    assert entity.count == 0
    assert not entity.has(CompA)
    assert not entity.has(CompB)


def test_add_comp_a():
    entity = Entity()
    entity.add(CompA, [])
    assert entity.count == 1
    assert entity.has(CompA)
    assert not entity.has(CompB)
    assert type(entity.get(CompA)) == CompA
    with pytest.raises(MissingComponent):
        entity.get(CompB)


def test_add_two_comp_a():
    entity = Entity()
    entity.add(CompA, [])
    with pytest.raises(AlreadyAddedComponent):
        entity.add(CompA, [])


def test_remove_comp_a():
    entity = Entity()
    entity.add(CompA, [])
    entity.remove(CompA)
    assert not entity.has(CompA)
    assert entity.count == 0
    with pytest.raises(MissingComponent):
        entity.remove(CompA)


def test_add_comp_b():
    entity = Entity()
    entity.add(CompB, [1, 2, 3])
    assert entity.get(CompB).x == 1
    assert entity.get(CompB).y == 2
    assert entity.get(CompB).z == 3


def test_replace_comp_b():
    entity = Entity()
    entity.add(CompB, [1, 2, 3])
    entity.replace(CompB, [4, 5, 6])
    assert entity.count == 1
    assert entity.get(CompB).x == 4
    assert entity.get(CompB).y == 5
    assert entity.get(CompB).z == 6

def test_destroy_entity():
    entity = Entity()
    entity.add(CompA, [])
    entity.add(CompB, [4, 5, 6])
    assert entity.count == 2
    entity.destroy()
    assert entity.count == 0
