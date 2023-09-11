from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Any, Callable

from pyplay.actor import Actors
from pyplay.log_book import LogBookRecord
from pyplay.play import Play
from pyplay.prop import PropFactories
from pyplay.stage import Stage

Narrator = Callable[[str], Any]


async def execute_play(play: Play, narrator: Narrator, prop_factories: PropFactories) -> None:
    log_book_records: list[LogBookRecord] = []

    async with AsyncExitStack() as exit_stack:
        stage = Stage(
            prop_factories=prop_factories,
            log_book_records=log_book_records,
            exit_stack=exit_stack
        )
        actors = Actors(
            exit_stack=exit_stack,
            log_book_records=log_book_records,
            prop_factories=prop_factories
        )

        for act in play:
            try:
                await act.action.execute(
                    actor=actors.get(act.character),
                    stage=stage
                )
            finally:
                narrator(act.narration())


def pyplay_spec(narrator: Narrator, prop_factories: PropFactories):
    def decorator(test_function: Callable):
        async def decorated(*args):
            play = Play()
            test_function(*args, play.character)
            await execute_play(play=play, narrator=narrator, prop_factories=prop_factories)

        decorated.__name__ = test_function.__name__

        return decorated

    return decorator
