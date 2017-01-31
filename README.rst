entitas-python
==============

.. image:: https://travis-ci.org/Aenyhm/entitas-python.svg?branch=master
    :target: https://travis-ci.org/Aenyhm/entitas-python

Entitas ECS implementation in Python.

Overview
--------

.. code-block:: python

  >>> Position = namedtuple('Position', ['x', 'y', 'z'])
  >>> context = entitas.Context()
  >>> entity = context.create_entity()
  >>> entity.add(Position, [1, 2, 3])
  <Entity_0 [Position(x=1, y=2, z=3)]>
  >>> entity.replace(Position, [4, 5, 6])
  <Entity_0 [Position(x=4, y=5, z=6)]>
  >>> entity.remove(Position)
  <Entity_0 []>
