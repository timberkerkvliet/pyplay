from __future__ import annotations

from unittest import IsolatedAsyncioTestCase

from pyplay.action import Assertion
from pyplay.action_executor import executes
from pyplay.play import Play

from pyplay.play_execution import execute_play


class OnePlusOneIsOne(Assertion):
    pass


@executes(OnePlusOneIsOne)
async def one_plus_one_is_one() -> None:
    assert 1 + 1 == 1


class TestFailingPlay(IsolatedAsyncioTestCase):
    async def test_failing_play_raises_assertion_error(self):
        play = Play()

        play.character('Timber').asserts(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await execute_play(play=play, narrator=print, prop_factories={}, action_executors=[one_plus_one_is_one])

    async def test_failing_play_narrates(self):
        narration_lines = []
        play = Play()

        play.character('Timber').asserts(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await execute_play(play=play, narrator=narration_lines.append, prop_factories={}, action_executors=[one_plus_one_is_one])

        self.assertEqual(len(narration_lines), 1)
        self.assertEqual(
            narration_lines[0],
            'Timber asserted OnePlusOneIsOne'
        )
