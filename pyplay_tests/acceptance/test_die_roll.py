from __future__ import annotations

import random
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action, Assertion
from pyplay.action_executor import executes
from pyplay.log_book import LogMessage, LogBook
from pyplay.play import CharacterCall
from pyplay.play_execution import pyplay_spec
from pyplay.logger import pyplay_logger


@dataclass(frozen=True)
class RolledTheDice(LogMessage):
    rolled: int


class RollTheDie(Action):
    def __str__(self) -> str:
        return f'rolled the die'


@executes(RollTheDie)
async def roll_the_die(log_book: LogBook) -> None:
    roll = random.randint(1, 6)

    log_book.write_message(RolledTheDice(rolled=roll))


class LastRollIsLessThan7(Assertion):
    def __str__(self) -> str:
        return 'last roll is less than 7'


@executes(LastRollIsLessThan7)
async def last_roll_less_than_7(log_book: LogBook) -> None:
    die_roll = log_book.find().by_type(RolledTheDice).last()

    assert die_roll.rolled < 7


my_spec = pyplay_spec(
    narrator=pyplay_logger(),
    prop_factories={},
    action_executors=[last_roll_less_than_7, roll_the_die]
)


class First(IsolatedAsyncioTestCase):
    @my_spec
    def test_a_die_rol(self, character: CharacterCall):
        character('Brian').performs(RollTheDie(), RollTheDie())
        character('Timber').asserts(LastRollIsLessThan7())
