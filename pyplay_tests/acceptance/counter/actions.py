from __future__ import annotations

from dataclasses import dataclass

from pyplay.action import Action, Assertion
from pyplay.action_executor import executes


from pyplay.prop import Props
from pyplay_tests.acceptance.counter.counter_app import App


class IncreaseCounter(Action):
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
