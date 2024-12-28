from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

import datetime
from enum import Enum

from app.database import Base, engine


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class UserRole(Enum):
    USER = "user"
    CEO = "ceo"
    SELLER = "seller"


class User(Base):
    __tablename__ = "users"

    fio: Mapped[str]
    login: Mapped[str]= mapped_column(unique=True)
    phone:Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    birthday: Mapped[datetime.datetime]= mapped_column(DateTime(timezone=True))
    gender: Mapped[Gender]
    address: Mapped[str]
    role: Mapped[UserRole]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


if __name__ == "__main__":
    Base.metadata.create_all(engine)
