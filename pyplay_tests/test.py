import random
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action, ExecutedAction
from pyplay.name import Name
from pyplay.expectation import Expectation
from pyplay.play import Play


@dataclass(frozen=True)
class RolledTheDice(ExecutedAction):
    actor_name: Name
    rolled: int

    def __str__(self) -> str:
        return f'{self.actor_name} rolled {self.rolled}'


class RollsTheDice(Action):
    async def execute(self, actor_name: Name) -> ExecutedAction:
        return RolledTheDice(
            actor_name=actor_name,
            rolled=random.randint(1, 6)
        )


class TheRollToBeLessThan7(Expectation):
    async def verify(self, executed_actions: ExecutedActions) -> None:
        ...


class First(IsolatedAsyncioTestCase):
    async def test_die_roll(self):
        play = Play(narrator=print)
        timber = play.with_actor_named('Timber')
        timber.performs(RollsTheDice())
        timber.expects(TheRollToBeLessThan7())
        await play.execute()
