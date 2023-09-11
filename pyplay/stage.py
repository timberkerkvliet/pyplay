from contextlib import AsyncExitStack
from typing import Type, TypeVar

from pyplay.log_book import LogBook, LogBookRecord
from pyplay.prop import PropFactory

T = TypeVar('T')


class Stage:
    def __init__(
        self,
        log_book_records: list[LogBookRecord],
        prop_factories: dict[type, PropFactory],
        exit_stack: AsyncExitStack
    ):
        self._log_book_records = log_book_records
        self._prop_factories = prop_factories
        self._props = {}
        self._exit_stack = exit_stack

    @property
    def log_book(self) -> LogBook:
        return LogBook(self._log_book_records)

    async def prop(self, prop_type: Type[T]) -> T:
        if prop_type not in self._props:
            prop_manager = self._prop_factories[prop_type]()
            self._props[prop_type] = await self._exit_stack.enter_async_context(prop_manager)

        return self._props[prop_type]
