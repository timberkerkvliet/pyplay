import importlib
import inspect
import pkgutil
from dataclasses import dataclass
from inspect import signature
from typing import Any, Protocol, Type

from pyplay.action import Action
from pyplay.actor import Actor
from pyplay.log_book import LogBook
from pyplay.prop import Props


class ActionExecutor(Protocol):
    async def __call__(self, action: Action, actor: Actor, stage_props: Props, log_book: LogBook) -> None:
        ...


class NormalizedExecutor:
    def __init__(self, executor):
        self._executor = executor
        self._args = set(dict(signature(executor).parameters).keys())

    async def __call__(self, action, actor, stage_props, log_book):
        kwargs = {
            'action': action,
            'actor': actor,
            'stage_props': stage_props,
            'log_book': log_book
        }
        kwargs = {k: v for k, v in kwargs.items() if k in self._args}
        return await self._executor(**kwargs)


@dataclass(frozen=True)
class RegisteredActionExecutor:
    action_type: Type[Action]
    executor: ActionExecutor


def executes(action_type: Type[Action]):
    def decorator(executor: ActionExecutor) -> RegisteredActionExecutor:
        return RegisteredActionExecutor(
            action_type=action_type,
            executor=NormalizedExecutor(executor)
        )

    return decorator


def find_executors_in_module(module: Any) -> list[RegisteredActionExecutor]:
    result: list[RegisteredActionExecutor] = []
    prefix = module.__name__ + "."
    for _, modname, ispkg in pkgutil.iter_modules(module.__path__, prefix):
        submodule = importlib.import_module(modname)
        if ispkg:
            result += find_executors_in_module(module=submodule)

            continue

        for member in inspect.getmembers(submodule):
            value = member[1]
            if isinstance(value, RegisteredActionExecutor):
                result.append(value)

    return result
