from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Any, Type, TypeVar

from pyplay.log_book import LogBookRecord, LogMessage
from pyplay.name import Name
from pyplay.prop import PropFactories

T = TypeVar('T')


class Actor:
    def __init__(
        self,
        name: Name,
        log_book_records: list[LogBookRecord],
        prop_factories: PropFactories,
        exit_stack: AsyncExitStack
    ):
        self._name = name
        self._exit_stack = exit_stack
        self._log_book_records = log_book_records
        self._prop_factories = prop_factories
        self._props: dict[type, Any] = {}

    @property
    def name(self) -> Name:
        return self._name

    def write_log_message(self, message: LogMessage) -> None:
        self._log_book_records.append(LogBookRecord(actor=self._name, message=message))

    async def prop(self, prop_type: Type[T]) -> T:
        if prop_type not in self._props:
            prop_manager = self._prop_factories[prop_type]()
            self._props[prop_type] = await self._exit_stack.enter_async_context(prop_manager)

        return self._props[prop_type]


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

    def get(self, name: Name) -> Actor:
        if name not in self._actors:
            self._actors[name] = Actor(
                exit_stack=self._exit_stack,
                name=name,
                log_book_records=self._log_book_records,
                prop_factories=self._prop_factories
            )

        return self._actors[name]
