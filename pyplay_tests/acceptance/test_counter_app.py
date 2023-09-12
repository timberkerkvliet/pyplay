from __future__ import annotations

from contextlib import asynccontextmanager
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Assertion
from pyplay.actor import Actor
from pyplay.play import CharacterCall
from pyplay.play_execution import pyplay_spec
from pyplay.stage import Stage


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
    async def execute(self, actor: Actor, stage: Stage) -> None:
        stage_app = await stage.prop(App)

        stage_app.increase_counter()


class CounterEquals(Assertion):
    def __init__(self, target: int):
        self._target = target

    async def execute(self, actor: Actor, stage: Stage) -> None:
        stage_app = await stage.prop(App)

        assert stage_app.get_counter() == self._target


my_spec = pyplay_spec(narrator=print, prop_factories={App: app})


class First(IsolatedAsyncioTestCase):
    @my_spec
    def test_the_app(self, character: CharacterCall):
        character('Brian').performs(IncreaseCounter())
        character('Timber').performs(IncreaseCounter())
        character('John').asserts(CounterEquals(2))
