from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Type, TypeVar

from pyplay.name import Name
from pyplay.play_notes import PlayNotes, Note, PlayNote
from pyplay.resource import Resource

T = TypeVar('T')


class Actor:
    def __init__(
        self,
        name: Name,
        play_notes: list[PlayNote],
        exit_stack: AsyncExitStack
    ):
        self._name = name
        self._play_notes = play_notes
        self._exit_stack = exit_stack
        self._resources: dict[type, Resource] = {}

    @property
    def name(self) -> Name:
        return self._name

    def write_note(self, note: Note) -> None:
        self._play_notes.append(
            PlayNote(actor=self._name, note=note)
        )

    @property
    def notes(self) -> PlayNotes:
        return PlayNotes(self._play_notes).by_actor(actor_name=self._name)

    async def get_resource(self, resource_type: Type[T]) -> T:
        if resource_type not in self._resources:
            resource = resource_type()
            self._resources[resource_type] = resource
            await self._exit_stack.enter_async_context(resource)

        return self._resources[resource_type]
