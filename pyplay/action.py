from __future__ import annotations

from abc import ABC, abstractmethod


class Action:
    def __str__(self):
        return self.__class__.__name__


class Assertion(Action, ABC):
    def __str__(self):
        return f'asserted {self.__class__.__name__}'
