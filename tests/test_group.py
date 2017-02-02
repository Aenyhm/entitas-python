# -*- coding: utf-8 -*-

from collections import namedtuple

import pytest

from entitas import Context, Matcher, Group, GroupSingleEntity


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
