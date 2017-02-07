# -*- coding: utf-8 -*-

from collections import namedtuple

import pytest

from entitas import Context, Matcher, GroupSingleEntity


CompA = namedtuple('CompA', [])


def test_single_entity():
    context = Context()
    entity = context.create_entity()
    entity.add(CompA)
    group = context.get_group(Matcher([CompA]))

    assert len(group.entities) == 1
    assert group.single_entity.has(CompA)


def test_not_single_entity():
    context = Context()

    entityA = context.create_entity()
    entityA.add(CompA)

    entityB = context.create_entity()
    entityB.add(CompA)

    group = context.get_group(Matcher([CompA]))

    assert len(group.entities) == 2
    with pytest.raises(GroupSingleEntity):
        group.single_entity.has(CompA)


def test_events():
    context = Context()
    group = context.get_group(Matcher([CompA]))
    entity = context.create_entity()
    entity.add(CompA)
    assert group.single_entity == entity
    entity.replace(CompA)
    assert group.single_entity == entity
    entity.remove(CompA)
    assert len(group.entities) == 0


def test_readme_example():
    context = Context()
    assert context.get_group(Matcher([CompA])).entities == []
    context.get_group(Matcher([CompA])).on_entity_added += lambda e: print(e)
    entity = context.create_entity()
    entity.add(CompA)
