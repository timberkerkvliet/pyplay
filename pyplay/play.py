from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Awaitable, NewType

from pyplay.action import Action
from pyplay.name import Name

from pyplay.play_execution import execute_play

Description = NewType('Description', str)
Part = Awaitable[Description]


@dataclass
class Act:
    character: Name
    action: Action


class Character:
    def __init__(self, name: Name, play: Play):
        self._name = name
        self._play = play

    def performs(self, *actions: Action) -> Character:
        for action in actions:
            self._play.acts.append(
                Act(character=self._name, action=action)
            )
        return self

    def asserts(self, *assertions) -> Character:
        return self.performs(*assertions)


CharacterCall = Callable[[Name], Character]


@dataclass
class Play:
    acts: list[Act] = field(default_factory=list)

    def character(self, name: Name) -> Character:
        return Character(name=name, play=self)

    def __iter__(self):
        return iter(self.acts)


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


def pyplay_spec(narrator):
    def decorator(test_function):
        async def decorated(*args):
            play = Play()
            test_function(*args, play.character)
            await execute_play(play=play, narrator=narrator)

        decorated.__name__ = test_function.__name__

        return decorated

    return decorator
