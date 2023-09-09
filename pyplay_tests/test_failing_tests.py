from __future__ import annotations

import random
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.ability import Abilities
from pyplay.action import Action
from pyplay.actor_action import ActorActions, ExecutedAction
from pyplay.assertion import Assertion, AssertionSuccessful, AssertionFailed
from pyplay.name import Name
from pyplay.play import pyplay_test, NewActor, Play


class OnePlusOneIsOne(Assertion):
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> None:
        assert 1 + 1 == 1


class TestFailingTests(IsolatedAsyncioTestCase):
    async def test_failing_test_raises_assertion_error(self):
        play = Play(print)

        timber = play.new_actor('Timber')
        timber.asserts(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await play.execute()

    async def test_failing_test_narrates(self):
        narration_lines = []
        play = Play(narration_lines.append)

        timber = play.new_actor('Timber')
        timber.asserts(OnePlusOneIsOne())

        with self.assertRaises(AssertionError):
            await play.execute()

        self.assertEqual(len(narration_lines), 1)
