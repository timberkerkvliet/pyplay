from __future__ import annotations

import random
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action, Assertion
from pyplay.actor import Actor
from pyplay.log_book import LogMessage
from pyplay.play import CharacterCall
from pyplay.play_execution import pyplay_spec
from pyplay.logger import pyplay_logger
from pyplay.stage import Stage


@dataclass(frozen=True)
class RolledTheDice(LogMessage):
    rolled: int


class RollTheDie(Action):
    async def execute(self, actor: Actor, stage: Stage) -> None:
        roll = random.randint(1, 6)

        actor.write_log_message(RolledTheDice(rolled=roll))

    def __str__(self) -> str:
        return f'rolled the die'


class LastRollIsLessThan7(Assertion):
    async def execute(self, actor: Actor, stage: Stage) -> None:
        die_roll = stage.log_book.by_type(RolledTheDice).last()

        assert die_roll.rolled < 7

    def __str__(self) -> str:
        return 'last roll is less than 7'


my_spec = pyplay_spec(narrator=pyplay_logger(), prop_factories={})


class First(IsolatedAsyncioTestCase):
    @my_spec
    def test_a_die_rol(self, character: CharacterCall):
        character('Brian').performs(RollTheDie(), RollTheDie())
        character('Timber').asserts(LastRollIsLessThan7())
