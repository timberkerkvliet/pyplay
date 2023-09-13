from dataclasses import dataclass
from inspect import signature
from typing import Protocol, Type, Callable, Awaitable

from pyplay.action import Action
from pyplay.actor import Actor
from pyplay.log_book import LogBook
from pyplay.prop import Props


class ActionExecutor(Protocol):
    async def __call__(self, action: Action, actor: Actor, stage_props: Props, log_book: LogBook) -> None:
        ...


@dataclass(frozen=True)
class RegisteredActionExecutor:
    action_type: Type[Action]
    executor: ActionExecutor


def executes(action_type):
    def decorator(executor: ActionExecutor) -> RegisteredActionExecutor:
        args = set(dict(signature(executor).parameters).keys())

        async def normalized_executor(action, actor, stage_props, log_book):
            kwargs = {
                'action': action,
                'actor': actor,
                'stage_props': stage_props,
                'log_book': log_book
            }
            kwargs = {k: v for k, v in kwargs.items() if k in args}
            return await executor(**kwargs)

        return RegisteredActionExecutor(
            action_type=action_type,
            executor=normalized_executor
        )

    return decorator
