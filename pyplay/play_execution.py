from contextlib import AsyncExitStack

from pyplay.actor import Actor
from pyplay.play import Play
from pyplay.stage import Stage


async def execute_play(play: Play, narrator) -> None:
    async with AsyncExitStack() as exit_stack:
        for act in play:
            action = act.action

            await action.execute(
                actor=Actor(
                    exit_stack=exit_stack,
                    name=act.character
                ),
                stage=Stage(
                    actor=act.character,
                    stage_notes=
                )
            )