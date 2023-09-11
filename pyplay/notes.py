from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pyplay.name import Name


class Note:
    """A note"""


T = TypeVar('T', bound=Note)
Y = TypeVar('Y', bound=Note)


class Notes(Generic[T]):
    def __init__(
        self,
        notes: list[T]
    ):
        self._notes = notes

    def by_type(self, note_type: Type[Y]) -> Notes[Y]:
        return Notes(
            [
                play_note for play_note in self._notes
                if isinstance(play_note, note_type)
            ]
        )

    def first(self) -> T:
        return self._notes[0]

    def last(self) -> T:
        return self._notes[-1]

    def one(self) -> T:
        if len(self._notes) != 1:
            raise Exception

        return self.first()


@dataclass(frozen=True)
class StageNote(Generic[T]):
    actor: Name
    note: T


class StageNotes(Generic[T]):
    def __init__(
        self,
        play_notes: list[StageNote[T]]
    ):
        self._play_notes = play_notes

    def by_type(self, action_type: Type[Y]) -> StageNotes[Y]:
        return StageNotes(
            [
                play_note for play_note in self._play_notes
                if isinstance(play_note.note, action_type)
            ]
        )

    def by_actor(self, actor_name: Name) -> StageNotes[T]:
        return StageNotes(
            [
                play_note for play_note in self._play_notes
                if play_note.actor == actor_name
            ]
        )

    def first(self) -> T:
        return self._play_notes[0].note

    def last(self) -> T:
        return self._play_notes[-1].note

    def one(self) -> T:
        if len(self._play_notes) != 1:
            raise Exception

        return self.first()
