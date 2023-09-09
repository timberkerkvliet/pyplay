from abc import ABC, abstractmethod

from pyplay.ability import Abilities
from pyplay.actor_action import ActorActions
from pyplay.name import Name


class Expectation(ABC):
    @abstractmethod
    async def verify(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> None:
        ...
