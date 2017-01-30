# -*- coding: utf-8 -*-

import pytest
from collections import namedtuple
from entitas import (
    Entity,
    ExistingComponentException,
    MissingComponentException)

CompA = namedtuple('CompA', [])
CompB = namedtuple('CompB', ['x', 'y', 'z'])


def test_create_entity():
    entity = Entity(2)
    assert entity.creation_index == 2
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
    with pytest.raises(MissingComponentException):
        entity.get(CompB)


def test_add_two_comp_a():
    entity = Entity()
    entity.add(CompA, [])
    with pytest.raises(ExistingComponentException):
        entity.add(CompA, [])


def test_remove_comp_a():
    entity = Entity()
    entity.add(CompA, [])
    entity.remove(CompA)
    assert not entity.has(CompA)
    assert entity.count == 0
    with pytest.raises(MissingComponentException):
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
