from __future__ import annotations

from unittest import IsolatedAsyncioTestCase

from pyplay.action import Expectation
from pyplay.action_executor import executes
from pyplay.play import Play

from pyplay.play_execution import execute_play


class OnePlusOneIsOne(Expectation):
    pass


@executes(OnePlusOneIsOne)
async def one_plus_one_is_one() -> None:
    assert 1 + 1 == 1


class TestFailingPlay(IsolatedAsyncioTestCase):
    def setUp(self):
        self.narration_lines = []

    async def execute_play(self, play: Play):
        await execute_play(
            play=play,
            narrator=self.narration_lines.append,
            prop_factories={},
            action_executors={OnePlusOneIsOne: one_plus_one_is_one.executor}
        )

    async def test_failing_play_raises_assertion_error(self):
        play = Play()

        play.character('Timber').expects(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await self.execute_play(play)

    async def test_failing_play_narrates(self):
        play = Play()

        play.character('Timber').expects(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await self.execute_play(play)

        self.assertEqual(len(self.narration_lines), 1)
        self.assertEqual(
            self.narration_lines[0],
            'Timber expected OnePlusOneIsOne'
        )
