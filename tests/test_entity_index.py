import pytest
from entitas import (
    Context, Matcher, PrimaryEntityIndex, EntityIndex, EntitasException
)
from .test_components import Person


class TestEntityIndex(object):

    def test_index(self):
        context = Context()
        group = context.get_group(Matcher(Person))
        index = EntityIndex(Person, group, 'age')
        context.add_entity_index(index)
        adam = context.create_entity()
        adam.add(Person, 'Adam', 42)
        eve = context.create_entity()
        eve.add(Person, 'Eve', 42)

        entities = context.get_entity_index(Person).get_entities(42)
        assert entities == set([adam, eve])

    def test_primary_index(self):
        context = Context()
        group = context.get_group(Matcher(Person))
        primary_index = PrimaryEntityIndex(Person, group, 'name')
        context.add_entity_index(primary_index)
        adam = context.create_entity()
        adam.add(Person, 'Adam', 42)
        eve = context.create_entity()
        eve.add(Person, 'Eve', 42)
        entity = context.get_entity_index(Person).get_entity('Eve')
        assert entity == eve

    def test_primary_index_exception(self):
        context = Context()
        group = context.get_group(Matcher(Person))
        primary_index = PrimaryEntityIndex(Person, group, 'age')
        context.add_entity_index(primary_index)
        adam = context.create_entity()
        adam.add(Person, 'Adam', 42)
        eve = context.create_entity()

        with pytest.raises(EntitasException):
            eve.add(Person, 'Eve', 42)
