from contextlib import asynccontextmanager
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from pyplay.action import Action, Assertion
from pyplay.action_executor import executes
from pyplay.actor import Actor
from pyplay.play import CharacterCall
from pyplay.play_execution import pyplay_spec
from pyplay.prop import Props


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


@asynccontextmanager
async def fake_mail_client():
    yield FakeMailClient()


@dataclass
class AddAsNewUser(Action):
    name: str


@executes(AddAsNewUser)
async def add_as_new_user(action: AddAsNewUser) -> None:
    FakeMailClient.send_mail(Mail(to=f'{action.name}@fake.com', body='Welcome'))


class ReceivedNotification(Assertion):
    pass


@executes(ReceivedNotification)
async def received_notification(actor: Actor, stage_props: Props) -> None:
    client = await stage_props(FakeMailClient)
    assert client.mails_for(f'{actor.character_name}@fake.com')


my_spec = pyplay_spec(
    narrator=print,
    prop_factories={FakeMailClient: fake_mail_client},
    action_executors=[received_notification, add_as_new_user]
)


class TestActorProp(IsolatedAsyncioTestCase):
    @my_spec
    def test_google_vist(self, character: CharacterCall):
        character('Brian').performs(
            AddAsNewUser('Timber')
        )
        character('Timber').asserts(ReceivedNotification())
