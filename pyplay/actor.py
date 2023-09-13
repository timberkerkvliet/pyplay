from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Any, Type, TypeVar

from pyplay.log_book import LogBookRecord, LogMessage
from pyplay.name import Name
from pyplay.prop import PropFactories, Props

T = TypeVar('T')


class Actor:
    def __init__(self, character_name: Name, props: Props):
        self._character_name = character_name
        self._props = props

    @property
    def character_name(self) -> Name:
        return self._character_name

    @property
    def props(self) -> Props:
        return self._props


class Actors:
    def __init__(
        self,
        exit_stack: AsyncExitStack,
        log_book_records: list[LogBookRecord],
        prop_factories: PropFactories
    ):
        self._actors: dict[Name, Actor] = {}
        self._exit_stack = exit_stack
        self._log_book_records = log_book_records
        self._prop_factories = prop_factories

    def get(self, character_name: Name) -> Actor:
        if character_name not in self._actors:
            self._actors[character_name] = Actor(
                props=Props(
                    exit_stack=self._exit_stack,
                    prop_factories=self._prop_factories
                ),
                character_name=character_name
            )

        return self._actors[character_name]
