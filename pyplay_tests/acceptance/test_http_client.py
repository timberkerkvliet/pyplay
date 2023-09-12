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
        self._visited_pages = []

    @property
    def visited_pages(self):
        return self._visited_pages

    async def get(self, page: str) -> None:
        self._visited_pages.append(page)


@asynccontextmanager
async def http_client():
    yield HTTPClient()


class VisitPage(Action):
    def __init__(self, page: str):
        self._page = page

    async def execute(self, actor: Actor, stage: Stage) -> None:
        client = await actor.prop(HTTPClient)
        await client.get(self._page)


class IVisitedPage(Assertion):
    def __init__(self, asserted_page: str):
        self._asserted_page = asserted_page

    async def execute(self, actor: Actor, stage: Stage) -> None:
        client = await actor.prop(HTTPClient)
        assert self._asserted_page in client.visited_pages


my_spec = pyplay_spec(narrator=print, prop_factories={HTTPClient: http_client})


class TestActorProp(IsolatedAsyncioTestCase):
    @my_spec
    def test_google_vist(self, actor: CharacterCall):
        actor('Brian').performs(VisitPage('google.com')).asserts(IVisitedPage('google.com'))
