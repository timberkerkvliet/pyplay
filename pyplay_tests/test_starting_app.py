from __future__ import annotations

import random
import uuid
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase
from uuid import UUID

from pyplay.action import Action
from pyplay.actor import Actor
from pyplay.assertion import Assertion, Asserted, FailedToAssert
from pyplay.name import Name
from pyplay.play import pyplay_spec, CharacterCall
from pyplay.play_notes import Note, PlayNotes


class App:
    def say_hello(self) -> str:
        return 'Hello world!'


class ItSaysHelloWorld(Assertion):
    async def execute(
        self,
        actor: Actor,
        play_notes: PlayNotes
    ) -> None:
        app = await actor.get_resource(App)

        assert 'Hello world' in app.say_hello()


class First(IsolatedAsyncioTestCase):
    @pyplay_spec
    def test_the_app(self, actor: CharacterCall):
        brain = actor('Brian')
        brain.asserts(ItSaysHelloWorld())
