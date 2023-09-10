from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pyplay.name import Name


class Note:
    """A note"""


T = TypeVar('T', bound=Note)
Y = TypeVar('Y', bound=Note)


@dataclass(frozen=True)
class PlayNote(Generic[T]):
    actor: Name
    note: T


class PlayNotes(Generic[T]):
    def __init__(
        self,
        play_notes: list[PlayNote[T]],
        actor_name: Name
    ):
        self._actor_name = actor_name
        self._play_notes = play_notes

    def by_type(self, action_type: Type[Y]) -> PlayNotes[Y]:
        return PlayNotes(
            [
                play_note for play_note in self._play_notes
                if isinstance(play_note.note, action_type)
            ],
            actor_name=self._actor_name
        )

    def by_actor(self, actor_name: Name) -> PlayNotes[T]:
        return PlayNotes(
            [
                play_note for play_note in self._play_notes
                if play_note.actor == actor_name
            ],
            actor_name=self._actor_name
        )

    def mine(self) -> PlayNotes[T]:
        return self.by_actor(self._actor_name)

    def first(self) -> T:
        return self._play_notes[0].note

    def last(self) -> T:
        return self._play_notes[-1].note

    def one(self) -> T:
        if len(self._play_notes) != 1:
            raise Exception

        return self.first()

    def add(self, note: Note) -> None:
        self._play_notes.append(
            PlayNote(
                actor=self._actor_name,
                note=note
            )
        )
