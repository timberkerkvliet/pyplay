from __future__ import annotations


class Action:
    def __str__(self):
        return self.__class__.__name__


class Expectation(Action):
    def __str__(self):
        return f'expected {self.__class__.__name__}'
