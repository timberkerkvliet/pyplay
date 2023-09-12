from contextlib import asynccontextmanager
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action, Assertion
from pyplay.actor import Actor
from pyplay.name import Name
from pyplay.play import CharacterCall
from pyplay.play_execution import pyplay_spec
from pyplay.stage import Stage


@dataclass(frozen=True)
class Mail:
    to: str
    body: str


class FakeMailClient:
    _sent_mails: list[Mail] = []

    @classmethod
    def mails_for(cls, address: str) -> list[Mail]:
        return [mail for mail in cls._sent_mails if mail.to == address]

    @classmethod
    def send_mail(cls, mail: Mail) -> None:
        cls._sent_mails.append(mail)


class AddAsNewUser(Action):
    def __init__(self, name: Name) -> None:
        self._name = name

    async def execute(self, actor: Actor, stage: Stage) -> None:
        FakeMailClient.send_mail(Mail(to=f'{self._name}@fake.com', body='Welcome'))


@asynccontextmanager
async def mail_client_prop():
    yield MailClient()


class ReceivedNotification(Assertion):

    async def execute(self, actor: Actor, stage: Stage) -> None:
        client = await stage.prop(FakeMailClient)
        assert client.mails_for()


my_spec = pyplay_spec(narrator=print, prop_factories={})


class TestActorProp(IsolatedAsyncioTestCase):
    @my_spec
    def test_google_vist(self, character: CharacterCall):
        character('Brian').performs(
            AddAsNewUser('Timber')
        )
        character('Timber').asserts(ReceivedNotification())
