from abc import ABC, abstractmethod

from pyplay.name import Name


class ExecutedAction:
    pass


class ExecutedActions:
    def __init__(self):
        ...


class Action(ABC):
    @abstractmethod
    async def execute(self, actor_name: Name) -> ExecutedAction:
        ...
