from pyplay.name import Name
from pyplay.notes import StageNotes, Note, StageNote


class Stage:
    def __init__(self, stage_notes: list[StageNote], actor: Name):
        self._stage_notes = stage_notes
        self._actor = actor

    @property
    def notes(self) -> StageNotes:
        return StageNotes(self._stage_notes)

    def write_note(self, note: Note) -> None:
        self._stage_notes.append(StageNote(actor=self._actor, note=note))

    async def resource(self, resource_type):
        ...
