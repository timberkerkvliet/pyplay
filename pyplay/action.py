from abc import ABC, abstractmethod
from actor import ActorName


class ExecutedAction(ABC):
    @abstractmethod
    def narrate(self, actor_name: ActorName) -> str:
        ...


class Action:
    async def execute(self) -> ExecutedAction:
        ...
