from __future__ import annotations

from unittest import IsolatedAsyncioTestCase

from pyplay.action_executor import find_executors_in_module
from pyplay.play import CharacterCall
from pyplay.play_execution import pyplay_spec
from pyplay_tests.acceptance import counter

from pyplay_tests.acceptance.counter.actions import CounterEquals, IncreaseCounter
from pyplay_tests.acceptance.counter.counter_app import App, app_prop

my_spec = pyplay_spec(
    narrator=print,
    prop_factories={App: app_prop},
    action_executors=find_executors_in_module(counter)
)


class TestCounterApp(IsolatedAsyncioTestCase):
    @my_spec
    def test_the_app(self, character: CharacterCall):
        character('Brian').performs(IncreaseCounter())
        character('Timber').performs(IncreaseCounter())
        character('John').asserts(CounterEquals(2))
