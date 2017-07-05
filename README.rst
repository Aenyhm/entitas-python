Entitas for Python
==================

.. image:: https://travis-ci.org/Aenyhm/entitas-python.svg?branch=master
    :target: https://travis-ci.org/Aenyhm/entitas-python

entitas-python is a port of `Entitas ECS for C# and Unity`_.


Overview
--------

Components
~~~~~~~~~~

.. code-block:: python

  Position = namedtuple('Position', 'x y')
  Health = namedtuple('Health', 'value')
  Movable = namedtuple('Movable', '')

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

  entities = context.entities
  for e in entities:
      # do something

Group
~~~~~

.. code-block:: python

  context.get_group(Matcher(Position)).entities

  def move(entity, new_comp):
      # do something

  context.get_group(Matcher(Position)).on_entity_added += move

Entity Collector
~~~~~~~~~~~~~~~~

.. code-block:: python

  group = context.get_group(Matcher(Position))
  collector = Collector()
  collector.add(group, GroupEvent.added)

  # later

  for e in collector.collected_entities:
     # do something with all the entities
     # that have been collected to this point of time

  collector.clear_collected_entities()

  # stop observing
  collector.deactivate()

Entity Index
~~~~~~~~~~~~

.. code-block:: python

  Person = namedtuple('Person', 'name age')
  group = context.get_group(Matcher(Person))

  # get a set of 42-year-old Person
  index = EntityIndex(Person, group, 'age')
  context.add_entity_index(index)
  entities = context.get_entity_index(Person).get_entities(42)

  # get the Person named "John"
  primary_index = PrimaryEntityIndex(Person, group, 'name')
  context.add_entity_index(primary_index)
  entity = context.get_entity_index(Person).get_entity('John')

Processors
~~~~~~~~~~

.. code-block:: python

  class RenderDisplay(ExecuteProcessor):

      def execute(self):
          pygame.display.update()


  # Initialize, Cleanup and TearDown are also available.


  class Move(ReactiveProcessor):

      def __init__(self, context):
          super().__init__(context)
          self._context = context

      def get_trigger(self):
          return {Matcher(Position): GroupEvent.ADDED}

      def filter(self, entity):
          return entity.has(Position, Movable)

      def react(self, entities):
          for entity in entities:
              # use entity.get(Position).x & entity.get(Position).y

Setup example
~~~~~~~~~~~~~

.. code-block:: python

  context = Context()

  processors = Processors()
  processors.add(StartGame(context))
  processors.add(InputProcessors(context))
  processors.add(RenderDisplay())
  processors.add(DestroyEntity(context))

  processors.initialize()
  processors.activate_reactive_processors()

  # main loop
  running = True
  while running:
      processors.execute()
      processors.cleanup()

      if EmitInput.quit:
          break

  processors.clear_reactive_processors()
  processors.tear_down()

  quit()


.. _Entitas ECS for C# and Unity : https://github.com/sschmid/Entitas-CSharp
