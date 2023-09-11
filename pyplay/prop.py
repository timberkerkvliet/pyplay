from typing import AsyncContextManager, Callable

PropManager = AsyncContextManager
PropFactory = Callable[[], PropManager]
PropFactories = dict[type, PropFactory]
