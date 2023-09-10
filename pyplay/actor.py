from __future__ import annotations

from typing import Type, TypeVar

from pyplay.name import Name
from pyplay.play_notes import PlayNotes, Note, PlayNote
from pyplay.resource import Resources

T = TypeVar('T')


class Actor:
    def __init__(
        self,
        name: Name,
        play_notes: list[PlayNote]
    ):
        self._name = name
        self._play_notes = play_notes
        self._resources = Resources()

    async def __aenter__(self):
        await self._resources.__aenter__()

    async def __aexit__(self, *args):
        await self._resources.__aexit__(args)

    @property
    def name(self) -> Name:
        return self._name

    def write_note(self, note: Note) -> None:
        self._play_notes.append(
            PlayNote(
                actor=self._name,
                note=note
            )
        )

    @property
    def notes(self) -> PlayNotes:
        return PlayNotes(self._play_notes).by_actor(actor_name=self._name)

    async def get_resource(self, resource_type: Type[T]) -> T:
        return await self._resources.get(resource_type)
