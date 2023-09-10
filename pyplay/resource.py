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

    async def get(self, resource_type: Type[T]) -> T:
        if resource_type not in self._resources:
            resource = resource_type()
            self._resources[resource_type] = resource



        filtered = [
            ability for ability in self._resources
            if isinstance(ability, resource_type)
        ]

        if len(filtered) != 1:
            raise Exception

        return filtered[0]
