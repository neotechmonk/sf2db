from typing import Any

from sqlalchemy import Column, Date, ForeignKey, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def to_dict(obj: Base) -> dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

