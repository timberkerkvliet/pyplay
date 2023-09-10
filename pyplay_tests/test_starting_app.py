from __future__ import annotations

import random
import uuid
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase
from uuid import UUID

from pyplay.ability import Abilities, Ability
from pyplay.action import Action, T
from pyplay.actor_action import ActorActions, ExecutedAction
from pyplay.assertion import Assertion, AssertedSuccessfully, FailedToAssert
from pyplay.name import Name
from pyplay.play import pyplay_test, NewActor


class App:
    def say_hello(self) -> str:
        return 'Hello world!'


@dataclass
class StartedTheApp(ExecutedAction):
    app: App

    def __str__(self):
        return 'started the app'


class StartTheApp(Action):
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> StartedTheApp:
        return StartedTheApp(App())


class ItSaysHelloWorld(Assertion):
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> None:
        app = action_history.by_action_type(StartedTheApp).one().app

        assert 'Hello world' in app.say_hello()


class First(IsolatedAsyncioTestCase):
    @pyplay_test
    def test_a_die_rol(self, actor: NewActor):
        brain = actor('Brian')
        brain.performs(StartTheApp())

        ana = actor('Ana')
        ana.asserts(ItSaysHelloWorld())
