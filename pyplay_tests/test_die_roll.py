from __future__ import annotations

import random
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action

from pyplay.assertion import Assertion
from pyplay.name import Name
from pyplay.play import pyplay_test, NewActor
from pyplay.play_notes import PlayNotes, Note
from pyplay.resource import Resources


@dataclass(frozen=True)
class RolledTheDice(Note):
    rolled: int


class RollTheDie(Action):
    async def execute(
        self,
        actor_name: Name,
        actor_resources: Resources,
        play_notes: PlayNotes
    ) -> None:
        roll = random.randint(1, 6)

        play_notes.add(
            RolledTheDice(rolled=roll)
        )

    def __str__(self) -> str:
        return f'rolled the die'


class TheRollIsLessThan7(Assertion):
    async def execute(
        self,
        actor_name: Name,
        actor_resources: Resources,
        play_notes: PlayNotes
    ) -> None:
        die_roll = play_notes.by_type(RolledTheDice).one()

        assert die_roll.rolled < 7

    def __str__(self) -> str:
        return 'roll is less than 7'


class First(IsolatedAsyncioTestCase):
    @pyplay_test
    def test_a_die_rol(self, actor: NewActor):
        actor('Timber') \
            .performs(RollTheDie()) \
            .asserts(TheRollIsLessThan7())
