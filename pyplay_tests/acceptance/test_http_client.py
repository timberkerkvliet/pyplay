from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action, Assertion
from pyplay.action_executor import executes
from pyplay.actor import Actor
from pyplay.play import CharacterCall
from pyplay.play_execution import pyplay_spec


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


@dataclass
class VisitPage(Action):
    page: str


@executes(VisitPage)
async def visit_page(action: VisitPage, actor: Actor) -> None:
    client = await actor.props(HTTPClient)
    await client.get(action.page)


@dataclass
class IVisitedPage(Assertion):
    page: str


@executes(IVisitedPage)
async def visited_page(action: IVisitedPage, actor: Actor) -> None:
    client = await actor.props(HTTPClient)
    assert action.page in client.visited_pages


my_spec = pyplay_spec(
    narrator=print,
    prop_factories={HTTPClient: http_client},
    action_executors=[visit_page, visited_page]
)


class TestActorProp(IsolatedAsyncioTestCase):
    @my_spec
    def test_google_vist(self, actor: CharacterCall):
        actor('Brian').performs(VisitPage('google.com')).asserts(IVisitedPage('google.com'))
