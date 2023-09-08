from abc import ABC, abstractmethod
from actor import ActorName


class PerformedAction(ABC):
    @abstractmethod
    def narrate(self, actor_name: ActorName) -> str:
        ...


class Action:
    async def perform(self) -> PerformedAction:
        ...
