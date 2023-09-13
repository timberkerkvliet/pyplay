from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Any, Callable, Type

from pyplay.action import Action
from pyplay.action_executor import ActionExecutor
from pyplay.actor import Actors
from pyplay.log_book import LogBookRecord, LogBook
from pyplay.play import Play
from pyplay.prop import PropFactories, Props

Narrator = Callable[[str], Any]


async def execute_play(
    play: Play,
    action_executors: dict[Type[Action], ActionExecutor],
    prop_factories: PropFactories,
    narrator: Narrator
) -> None:
    log_book_records: list[LogBookRecord] = []

    async with AsyncExitStack() as exit_stack:
        stage_props = Props(
            prop_factories=prop_factories,
            exit_stack=exit_stack
        )
        actors = Actors(
            exit_stack=exit_stack,
            log_book_records=log_book_records,
            prop_factories=prop_factories
        )

        for act in play:
            executor = action_executors[type(act.action)]
            try:
                await executor(
                    action=act.action,
                    actor=actors.get(act.character),
                    stage_props=stage_props,
                    log_book=LogBook(records=log_book_records, actor_name=act.character)
                )
            finally:
                narrator(act.narration())


def pyplay_spec(narrator: Narrator, action_executors, prop_factories: PropFactories):
    action_executors = {
        v.action_type: v.executor
        for v in action_executors
    }

    def decorator(test_function: Callable):
        async def decorated(*args):
            play = Play()
            test_function(*args, play.character)
            await execute_play(
                play=play,
                narrator=narrator,
                prop_factories=prop_factories,
                action_executors=action_executors
            )

        decorated.__name__ = test_function.__name__

        return decorated

    return decorator
