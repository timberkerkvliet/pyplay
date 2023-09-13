from contextlib import asynccontextmanager


class App:
    def __init__(self):
        self._counter = 0

    def increase_counter(self) -> None:
        self._counter += 1

    def get_counter(self) -> int:
        return self._counter


@asynccontextmanager
async def app_prop():
    yield App()
