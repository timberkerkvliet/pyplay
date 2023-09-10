from __future__ import annotations

from unittest import IsolatedAsyncioTestCase

from pyplay.actor import Actor
from pyplay.assertion import Assertion
from pyplay.play import Play
from pyplay.play_notes import PlayNotes


class OnePlusOneIsOne(Assertion):
    async def execute(
        self,
        actor: Actor,
        play_notes: PlayNotes
    ) -> None:
        assert 1 + 1 == 1


class TestFailingPlay(IsolatedAsyncioTestCase):
    async def test_failing_play_raises_assertion_error(self):
        play = Play(print)

        play.actor('Timber').asserts(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await play.execute()

    async def test_failing_play_narrates(self):
        narration_lines = []
        play = Play(narration_lines.append)

        play.actor('Timber').asserts(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await play.execute()

        self.assertEqual(len(narration_lines), 1)
