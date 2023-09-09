import random
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.ability import Abilities
from pyplay.action import Action, ExecutedAction, ActorActions
from pyplay.name import Name
from pyplay.expectation import Expectation
from pyplay.play import pyplay_test, NewActor


@dataclass(frozen=True)
class RolledTheDice(ExecutedAction):
    actor_name: Name
    rolled: int

    def __str__(self) -> str:
        return f'{self.actor_name} rolled {self.rolled}'


class RollsTheDice(Action):
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> ExecutedAction:
        return RolledTheDice(
            actor_name=actor_name,
            rolled=random.randint(1, 6)
        )


class TheRollToBeLessThan7(Expectation):
    async def verify(self) -> None:
        ...


class First(IsolatedAsyncioTestCase):
    @pyplay_test
    def test_this_one(self, new_actor: NewActor):
        timber = new_actor('Timber')
        timber.performs(RollsTheDice())
        timber.expects(TheRollToBeLessThan7())
