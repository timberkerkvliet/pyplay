from __future__ import annotations

from contextlib import asynccontextmanager
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action, Assertion
from pyplay.actor import Actor
from pyplay.play import CharacterCall
from pyplay.play_execution import pyplay_spec
from pyplay.stage import Stage


class HTTPClient:
    def __init__(self):
        self.entered = False
        self.exited = False
        self.logged_in = False

    async def __aenter__(self):
        self.entered = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.exited = True

    async def login(self) -> None:
        self.logged_in = True


def http_client():
    return HTTPClient()


class Login(Action):
    async def execute(self, actor: Actor, stage: Stage) -> None:
        client = await actor.prop(HTTPClient)
        await client.login()


class IsLoggedIn(Assertion):
    async def execute(self, actor: Actor, stage: Stage) -> None:
        client = await actor.prop(HTTPClient)
        assert client.logged_in


class IsNotLoggedIn(Assertion):
    async def execute(self, actor: Actor, stage: Stage) -> None:
        client = await actor.prop(HTTPClient)
        assert not client.logged_in


my_spec = pyplay_spec(narrator=print, prop_factories={HTTPClient: http_client})


class TestActorProp(IsolatedAsyncioTestCase):
    @my_spec
    def test_actor_prop(self, actor: CharacterCall):
        actor('Brian').performs(Login()).asserts(IsLoggedIn())
        actor('Pim').asserts(IsNotLoggedIn())
