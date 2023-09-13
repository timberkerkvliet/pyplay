from contextlib import AsyncExitStack
from typing import AsyncContextManager, Callable, TypeVar, Type

PropManager = AsyncContextManager
PropFactory = Callable[[], PropManager]
PropFactories = dict[type, PropFactory]


T = TypeVar('T')


class Props:
    def __init__(
        self,
        prop_factories: dict[type, PropFactory],
        exit_stack: AsyncExitStack
    ):
        self._prop_factories = prop_factories
        self._exit_stack = exit_stack
        self._props = {}

    async def __call__(self, prop_type: Type[T]) -> T:
        if prop_type not in self._props:
            prop_manager = self._prop_factories[prop_type]()
            self._props[prop_type] = await self._exit_stack.enter_async_context(prop_manager)

        return self._props[prop_type]
