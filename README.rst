entitas-python
==============

.. image:: https://travis-ci.org/Aenyhm/entitas-python.svg?branch=master
    :target: https://travis-ci.org/Aenyhm/entitas-python

entitas-python aims to be a port of `Entitas ECS for C# and Unity`_.

Overview
--------

Entity
~~~~~~

.. code-block:: python

  entity.add(Position, 3, 7)
  entity.add(Health, 100)
  entity.add(Movable)

  entity.replace(Position, 10, 100)
  entity.replace(Health, entity.get(Health).value - 1)

  entity.remove(Position)

  has_pos = entity.has(Position)
  movable = entity.has(Movable)

Context
~~~~~~~

.. code-block:: python

  context = Context()
  entity = context.create_entity()
  entity.add(Movable)

  entities = context.get_entities(Matcher(all_of=[Movable, Position]))
  for e in entities:
      # do something


.. _Entitas ECS for C# and Unity : https://github.com/sschmid/Entitas-CSharp
