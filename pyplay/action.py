from abc import ABC, abstractmethod


class ExecutedAction:
    pass


class Action(ABC):
    @abstractmethod
    async def execute(self) -> ExecutedAction:
        ...
