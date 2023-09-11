from __future__ import annotations

import random
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action
from pyplay.actor import Actor
from pyplay.assertion import Assertion
from pyplay.play import pyplay_spec, CharacterCall, pyplay_log_narrator
from pyplay.play_notes import PlayNotes, Note


@dataclass(frozen=True)
class RolledTheDice(Note):
    rolled: int


class RollTheDie(Action):
    async def execute(self, actor: Actor, play_notes: PlayNotes) -> None:
        roll = random.randint(1, 6)

        actor.write_note(RolledTheDice(rolled=roll))

    def __str__(self) -> str:
        return f'rolled the die'


class LastRollIsLessThan7(Assertion):
    async def execute(self, actor: Actor, play_notes: PlayNotes) -> None:
        die_roll = actor.notes.by_type(RolledTheDice).last()

        assert die_roll.rolled < 7

    def __str__(self) -> str:
        return 'roll is less than 7'


my_spec = pyplay_spec(narrator=pyplay_log_narrator())


class First(IsolatedAsyncioTestCase):
    @my_spec
    def test_a_die_rol(self, actor: CharacterCall):
        actor('Timber').performs(RollTheDie(), RollTheDie())
        actor('Timber').asserts(LastRollIsLessThan7())
