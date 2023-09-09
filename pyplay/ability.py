from typing import AsyncContextManager, TypeVar, Type


class Ability(AsyncContextManager):
    async def __aenter__(self):
        ...

    async def __aexit__(self, *args) -> None:  # type: ignore
        return


T = TypeVar('T', bound=Ability)


class Abilities:
    def __init__(self, abilities):
        self._abilities = abilities

    def add(self, ability: Ability):
        self._abilities.append(ability)

    def get(self, ability_type: Type[T]) -> T:
        filtered = [
            ability for ability in self._abilities
            if isinstance(ability, ability_type)
        ]

        if len(filtered) != 1:
            raise Exception

        return filtered[0]
