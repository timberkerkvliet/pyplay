from __future__ import annotations

from dataclasses import dataclass

from pyplay.action import Action
from pyplay.name import Name


@dataclass(frozen=True)
class Act:
    character: Name
    action: Action
    is_attempt: bool

    def narration(self) -> str:
        return f'{self.character} {self.action}'
