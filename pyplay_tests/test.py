from __future__ import annotations

import random
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.ability import Abilities
from pyplay.action import Action
from pyplay.actor_action import ActorActions, ExecutedAction
from pyplay.assertion import Assertion, AssertedSuccessfully, FailedToAssert
from pyplay.name import Name
from pyplay.play import pyplay_test, NewActor


@dataclass(frozen=True)
class RolledTheDice(ExecutedAction):
    rolled: int

    def __str__(self) -> str:
        return f'rolled {self.rolled}'


class RollTheDice(Action):
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> ExecutedAction:
        roll = random.randint(1, 6)
        return RolledTheDice(rolled=roll)


class TheRollToBeLessThan7(Assertion):
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> None:
        die_roll = action_history\
            .by_actor(actor_name)\
            .by_action_type(RolledTheDice)\
            .first()

        assert die_roll.rolled < 7


class First(IsolatedAsyncioTestCase):
    @pyplay_test
    def test_a_die_rol(self, new_actor: NewActor):
        timber = new_actor('Timber')
        timber.performs(RollTheDice())
        timber.asserts(TheRollToBeLessThan7())
