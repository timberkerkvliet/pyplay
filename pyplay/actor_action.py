from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pyplay.name import Name


class Note:
    """Describes an action that was executed."""


T = TypeVar('T', bound=Note)
Y = TypeVar('Y', bound=Note)


@dataclass(frozen=True)
class PlayNote(Generic[T]):
    actor_name: Name
    note: T

    def narration(self) -> str:
        return f'{self.actor_name} {self.note}'


class PlayNotes(Generic[T]):
    def __init__(self, actor_actions: list[PlayNote[T]]):
        self._actor_actions = actor_actions

    def by_type(self, action_type: Type[Y]) -> PlayNotes[Y]:
        return PlayNotes(
            [
                actor_action for actor_action in self._actor_actions
                if isinstance(actor_action.note, action_type)
            ]
        )

    def by_actor(self, actor_name: Name) -> PlayNotes[T]:
        return PlayNotes(
            [
                actor_action for actor_action in self._actor_actions
                if actor_action.actor_name == actor_name
            ]
        )

    def first(self) -> T:
        return self._actor_actions[0].note

    def last(self) -> T:
        return self._actor_actions[-1].note

    def one(self) -> T:
        if len(self._actor_actions) != 1:
            raise Exception

        return self.first()

    def add(self, author: Name, note: Note) -> None:
        self._actor_actions.append(
            PlayNote(
                actor_name=author,
                note=note
            )
        )
