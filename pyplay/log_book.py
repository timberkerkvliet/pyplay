from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, Type, TypeVar

from pyplay.name import Name


class LogMessage:
    """A note"""


T = TypeVar('T', bound=LogMessage)
Y = TypeVar('Y', bound=LogMessage)


@dataclass(frozen=True)
class LogBookRecord(Generic[T]):
    actor: Name
    message: T


class LogBook(Generic[T]):
    def __init__(self, records: list[LogBookRecord[T]]):
        self._records = records

    def by_type(self, action_type: Type[Y]) -> LogBook[Y]:
        return LogBook(
            [
                record for record in self._records
                if isinstance(record.message, action_type)
            ]
        )

    def by_actor(self, actor_name: Name) -> LogBook[T]:
        return LogBook(
            [
                record for record in self._records
                if record.actor == actor_name
            ]
        )

    def first(self) -> T:
        return self._records[0].message

    def last(self) -> T:
        return self._records[-1].message

    def one(self) -> T:
        if len(self._records) != 1:
            raise Exception

        return self.first()

    def __iter__(self) -> Iterator[LogBookRecord]:
        return iter(self._records)
