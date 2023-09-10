from __future__ import annotations

from pyplay.action import Action
from pyplay.actor_action import PlayNotes
from pyplay.assertion import Assertion, FailedToAssert, Asserted
from pyplay.name import Name
from pyplay.resource import Resources


class Actor:
    def __init__(
        self,
        name: Name,
        resources: Resources,
        add_part,
        play_notes: PlayNotes
    ) -> None:
        self._name = name
        self._resources = resources
        self._add_part = add_part
        self._play_notes = play_notes

    @property
    def name(self) -> Name:
        return self._name

    async def _perform_action(self, action: Action) -> None:
        notes = await action.execute(
            actor_name=self._name,
            actor_resources=self._resources,
            play_notes=self._play_notes
        )
        for note in notes:
            self._play_notes.add(
                author=self._name,
                note=note
            )

    async def _assert(self, assertion: Assertion) -> None:
        try:
            await assertion.execute(
                actor_name=self._name,
                actor_resources=self._resources,
                play_notes=self._play_notes
            )
        except AssertionError:
            pass
            raise
        else:
            pass

    def performs(self, *actions: Action) -> Actor:
        for action in actions:
            self._add_part(self._perform_action(action))
        return self

    def asserts(self, *assertions) -> Actor:
        for assertion in assertions:
            self._add_part(self._assert(assertion))
        return self
