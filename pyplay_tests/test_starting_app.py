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


@dataclass
class ControlTheApp(Ability):
    def start(self):
        return random.randint(1, 6)


@dataclass
class UseTheApp(Ability):
    def start(self):
        return random.randint(1, 6)


@dataclass
class StartedTheApp(ExecutedAction):
    app_id: UUID

    def __str__(self):
        return 'started the app'


class StartTheApp(Action):
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> StartedTheApp:
        return StartedTheApp(uuid.uuid4())


class HelloWorld(Assertion):
    async def execute(
        self,
        actor_name: Name,
        actor_abilities: Abilities,
        action_history: ActorActions
    ) -> None:
        app_id = action_history.by_action_type(StartedTheApp).one().app_id

        assert app_id is not None


class First(IsolatedAsyncioTestCase):
    @pyplay_test
    def test_a_die_rol(self, actor: NewActor):
        brain = actor('Brian').who_can(ControlTheApp())
        brain.performs(StartTheApp())

        ana = actor('Ana').who_can(UseTheApp())
        ana.asserts(HelloWorld())
