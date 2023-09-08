from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action, ExecutedAction
from pyplay.actor import ActorName
from pyplay.play import Play


@dataclass(frozen=True)
class RolledTheDice(ExecutedAction):
    actor_name: ActorName
    rolled: int

    def __str__(self) -> str:
        return f'{self.actor_name} rolled {int}'


class RollsTheDice(Action):
    async def execute(self) -> ExecutedAction:
        pass


class TheRollToBeLessThan7:
    async def verify(self) -> None:
        ...


class First(IsolatedAsyncioTestCase):
    async def test(self):
        play = Play(narrator=print)
        timber = play.with_actor(ActorName('Timber'))

        timber.performs(RollsTheDice())

        timber.expects(TheRollToBeLessThan7())

        await play.perform()
