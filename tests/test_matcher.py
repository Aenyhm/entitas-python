from collections import namedtuple
from entitas import Entity, Matcher

CompA = namedtuple('CompA', '')
CompB = namedtuple('CompB', '')
CompC = namedtuple('CompC', '')
CompD = namedtuple('CompD', '')
CompE = namedtuple('CompE', '')
CompF = namedtuple('CompF', '')


def test_matches():
    ea = Entity()
    eb = Entity()
    ec = Entity()
    ea.activate(0)
    eb.activate(1)
    ec.activate(2)
    ea.add(CompA)
    ea.add(CompB)
    ea.add(CompC)
    ea.add(CompE)
    eb.add(CompA)
    eb.add(CompB)
    eb.add(CompC)
    eb.add(CompE)
    eb.add(CompF)
    ec.add(CompB)
    ec.add(CompC)
    ec.add(CompD)

    matcher = Matcher(all_of=[CompA, CompB, CompC],
                      any_of=[CompD, CompE],
                      none_of=[CompF])

    assert matcher.matches(ea)
    assert not matcher.matches(eb)
    assert not matcher.matches(ec)
