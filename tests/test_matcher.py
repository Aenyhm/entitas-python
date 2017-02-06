# -*- coding: utf-8 -*-

from collections import namedtuple

from entitas import Entity, Matcher


CompA = namedtuple('CompA', [])
CompB = namedtuple('CompB', [])
CompC = namedtuple('CompC', [])
CompD = namedtuple('CompD', [])
CompE = namedtuple('CompE', [])
CompF = namedtuple('CompF', [])


def test_matches():
    eA = Entity()
    eB = Entity()
    eC = Entity()

    eA.activate(0)
    eB.activate(1)
    eC.activate(2)
    eA.add(CompA); eA.add(CompB); eA.add(CompC); eA.add(CompE)
    eB.add(CompA); eB.add(CompB); eB.add(CompC); eB.add(CompE); eB.add(CompF)
    eC.add(CompB); eC.add(CompC); eC.add(CompD)

    matcher = Matcher(all_of=[CompA, CompB, CompC],
                      any_of=[CompD, CompE],
                      none_of=[CompF])

    assert matcher.matches(eA)
    assert not matcher.matches(eB)
    assert not matcher.matches(eC)
