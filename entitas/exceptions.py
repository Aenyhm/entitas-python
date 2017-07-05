class EntityNotEnabled(Exception):
    """The entity is not enabled."""


class AlreadyAddedComponent(Exception):
    """The entity already contains this type of component."""


class MissingComponent(Exception):
    """The entity does not contain this type of component."""


class MissingEntity(Exception):
    """The context does not contain this entity."""


class GroupSingleEntity(Exception):
    """The group contains more than one entity."""


class EntitasException(Exception):
    def __init__(self, message, hint):
        super().__init__(message + '\n' + hint if hint else message)
