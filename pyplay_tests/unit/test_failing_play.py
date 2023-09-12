from __future__ import annotations

from unittest import IsolatedAsyncioTestCase

from pyplay.action import Assertion
from pyplay.actor import Actor
from pyplay.play import Play

from pyplay.play_execution import execute_play
from pyplay.stage import Stage


class OnePlusOneIsOne(Assertion):
    async def execute(self, actor: Actor, stage: Stage) -> None:
        assert 1 + 1 == 1


class TestFailingPlay(IsolatedAsyncioTestCase):
    async def test_failing_play_raises_assertion_error(self):
        play = Play()

        play.character('Timber').asserts(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await execute_play(play=play, narrator=print, prop_factories={})

    async def test_failing_play_narrates(self):
        narration_lines = []
        play = Play()

        play.character('Timber').asserts(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await execute_play(play=play, narrator=narration_lines.append, prop_factories={})

        self.assertEqual(len(narration_lines), 1)
        self.assertEqual(
            narration_lines[0],
            'Timber asserted OnePlusOneIsOne'
        )
