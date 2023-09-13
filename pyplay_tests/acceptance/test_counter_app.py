from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Assertion
from pyplay.action_executor import executes
from pyplay.play import CharacterCall
from pyplay.play_execution import pyplay_spec


from pyplay.prop import Props


class App:
    def __init__(self):
        self._counter = 0

    def increase_counter(self) -> None:
        self._counter += 1

    def get_counter(self) -> int:
        return self._counter


@asynccontextmanager
async def app():
    yield App()


class IncreaseCounter(Assertion):
    pass


@executes(IncreaseCounter)
async def increase_counter(stage_props: Props) -> None:
    stage_app = await stage_props(App)

    stage_app.increase_counter()


@dataclass
class CounterEquals(Assertion):
    target: int


@executes(CounterEquals)
async def counter_equals(action: CounterEquals, stage_props: Props) -> None:
    stage_app = await stage_props(App)

    assert stage_app.get_counter() == action.target


my_spec = pyplay_spec(
    narrator=print,
    prop_factories={App: app},
    action_executors=[counter_equals, increase_counter]
)


class First(IsolatedAsyncioTestCase):
    @my_spec
    def test_the_app(self, character: CharacterCall):
        character('Brian').performs(IncreaseCounter())
        character('Timber').performs(IncreaseCounter())
        character('John').asserts(CounterEquals(2))
