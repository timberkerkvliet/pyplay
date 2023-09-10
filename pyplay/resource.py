from contextlib import AsyncExitStack
from typing import AsyncContextManager, TypeVar, Type


class Resource(AsyncContextManager):
    async def __aenter__(self):
        ...

    async def __aexit__(self, *args) -> None:  # type: ignore
        return


T = TypeVar('T', bound=Resource)


class Resources:
    def __init__(self):
        self._resources: dict[type, Resource] = {}

    async def __aenter__(self):
        self._exit_stack = AsyncExitStack()
        await self._exit_stack.__aenter__()

    async def __aexit__(self, *args):
        await self._exit_stack.__aexit__(*args)

    async def get(self, resource_type: Type[T]) -> T:
        if resource_type not in self._resources:
            resource = resource_type()
            self._resources[resource_type] = resource
            await self._exit_stack.enter_async_context(resource)

        return self._resources[resource_type]
