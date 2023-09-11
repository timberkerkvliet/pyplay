from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Type, TypeVar

from pyplay.name import Name
from pyplay.play_notes import Note, Notes
from pyplay.resource import Resource

T = TypeVar('T')


class Actor:
    def __init__(
        self,
        name: Name,
        exit_stack: AsyncExitStack
    ):
        self._name = name
        self._notes: list[Note] = []
        self._exit_stack = exit_stack
        self._resources: dict[type, Resource] = {}

    @property
    def name(self) -> Name:
        return self._name

    def write_note(self, note: Note) -> None:
        self._notes.append(note)

    @property
    def notes(self) -> Notes:
        return Notes(self._notes)

    async def get_resource(self, resource_type: Type[T]) -> T:
        if resource_type not in self._resources:
            resource = resource_type()
            self._resources[resource_type] = resource
            await self._exit_stack.enter_async_context(resource)

        return self._resources[resource_type]
