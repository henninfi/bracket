from heliclockter import datetime_utc

from bracket.models.db.shared import BaseModelORM
from bracket.utils.id_types import ClubId

from uuid import UUID


class Club(BaseModelORM):
    id: ClubId | None = None
    name: str
    created: datetime_utc


class ClubCreateBody(BaseModelORM):
    name: str
    id: UUID


class ClubUpdateBody(BaseModelORM):
    name: str
