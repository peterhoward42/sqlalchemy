from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import Session

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

engine = create_engine("sqlite://", echo=True)


class Base(DeclarativeBase):
    pass


""" Native SQLAlchemy to define mapped database classes."""


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    # A 1:many relationship field. Also provides reverse mapping field name.
    # Note the "cascade" property for configure deletion behaviour.
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    # Explicit foreign key field. Note the use "id" in the field name, and the target at the user end.
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    # Exposed 1:1 relationship field.
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# How you register the models with the engine and thus imply DDL.
Base.metadata.create_all(engine)

# Create a context-managed session.
with Session(engine) as session:
    # Standard python construction.
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")

    # Tell the session to include the objects created above and to commit them.
    session.add_all([spongebob, sandy, patrick])
    session.commit()

    # Illustrates select-where
    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
    # I think scalars() is telling the engine to return an iterator / cursor.
    for user in session.scalars(stmt):
        print(user)

    # Selecting over a Join
    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == "sandy")
        .where(Address.email_address == "sandy@sqlalchemy.org")
    )
    sandy_address = session.scalars(stmt).one()
    print(sandy_address)

    # Mutate the python objects that the session has registered already.
    stmt = select(User).where(User.name == "patrick")
    patrick = session.scalars(stmt).one()
    # Standard python list append.
    patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
    sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

    # commit() will flush the changes to the database.
    session.commit()

    print("\nXXXX deletion\n")
    # Remove one of Sandy's addresses.
    sandy = session.get(User, 2)
    sandy.addresses.remove(sandy_address)
    # Remove patrick entirely (likely deletes his addresses too)
    session.delete(patrick)

    session.commit()
