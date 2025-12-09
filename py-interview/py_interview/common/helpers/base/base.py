import uuid
from dataclasses import dataclass, field
import datetime as dt

__all__ = ['Base', 'fake_base', 'create_base']


@dataclass(frozen=True, slots=True, kw_only=True)
class Base:
    uqid: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: dt.datetime = dt.datetime.now()
    created_by: str = 'unknown'
    updated_at: dt.datetime = dt.datetime.now()
    updated_by: str = 'unknown'


def fake_base(uqid: str = uuid.uuid4(), created_at: dt.datetime = None,
              created_by: str = 'unit-test-1', updated_at: dt.datetime = None,
              updated_by: str = 'unit-test-1') -> Base:
    return Base(uqid=uqid, created_at=created_at, created_by=created_by, updated_at=updated_at,
                updated_by=updated_by)


def create_base(user: str) -> Base:
    now = dt.datetime.now()
    return Base(uqid=str(uuid.uuid4()), created_at=now, created_by=user, updated_at=now, updated_by=user)
