from abc import ABC, abstractmethod


class Expectation(ABC):
    @abstractmethod
    async def verify(self) -> None:
        ...
