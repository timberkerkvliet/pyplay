from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Callable, Awaitable, NewType, AsyncGenerator

from pyplay.actor import Actor
from pyplay.actor_action import PlayNotes
from pyplay.name import Name
from pyplay.resource import Resources

Description = NewType('Description', str)
Part = Awaitable[Description]

NewActor = Callable[[Name], Actor]


class Play:
    def __init__(self, narrator: Callable[[str], None] | None):
        self._narrator: Callable[[str], None] | None = narrator
        self._actors: dict[Name, Actor] = {}
        self._parts: list[Part] = []
        self._notes = PlayNotes([])

    def actor(self, name: Name) -> Actor:
        if name not in self._actors:
            self._actors[name] = Actor(
                name=name,
                resources=Resources(),
                add_part=self._parts.append,
                play_notes=self._notes
            )

        return self._actors[name]

    async def execute(self) -> None:
        try:
            for part in self._parts:
                await part
        finally:
            pass


def pyplay_log_narrator():
    logger = logging.getLogger('pyplay')
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter(f'[%(asctime)s] [pyplay] %(message)s')
    )
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger.info


def pyplay_test(test_function):
    async def decorated(*args):
        play = Play(narrator=pyplay_log_narrator())
        test_function(*args, play.actor)
        await play.execute()

    decorated.__name__ = test_function.__name__

    return decorated
