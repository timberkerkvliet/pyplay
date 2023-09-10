from __future__ import annotations

import random
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action
from pyplay.actor import Actor

from pyplay.assertion import Assertion
from pyplay.name import Name
from pyplay.play import pyplay_spec, ActorCall
from pyplay.play_notes import PlayNotes, Note
from pyplay.resource import Resources


@dataclass(frozen=True)
class RolledTheDice(Note):
    rolled: int


class RollTheDie(Action):
    async def execute(
        self,
        actor: Actor,
        play_notes: PlayNotes
    ) -> None:
        roll = random.randint(1, 6)

        actor.write_note(
            RolledTheDice(rolled=roll)
        )

    def __str__(self) -> str:
        return f'rolled the die'


class TheRollIsLessThan7(Assertion):
    async def execute(
        self,
        actor: Actor,
        play_notes: PlayNotes
    ) -> None:
        die_roll = play_notes.by_type(RolledTheDice).one()

        assert die_roll.rolled < 7

    def __str__(self) -> str:
        return 'roll is less than 7'


class First(IsolatedAsyncioTestCase):
    @pyplay_spec
    def test_a_die_rol(self, actor: ActorCall):
        actor('Timber').performs(RollTheDie())
        actor('Timber').asserts(TheRollIsLessThan7())
