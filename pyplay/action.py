from abc import ABC, abstractmethod
from actor import ActorName


class ExecutedAction:
    pass


class Action(ABC):
    @abstractmethod
    async def execute(self) -> ExecutedAction:
        ...
