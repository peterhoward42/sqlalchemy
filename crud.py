from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
Session = sessionmaker(engine)


class User:
    pass


def run():

    with Session(engine) as session:
        """
        Functional composition of query statement.
        Return type inference as Select[Tuple[User]]

        scalars() fetches one row (the first), from a set of rows.
        I recall that all() enumerates the cursor.
        """
        statement = select(User).filter_by(name="ed")
        user_obj = session.scalars(statement).all()

        """
        Get some columns for the User table.
        """
        statement = select(User.name, User.fullname)
        rows = session.execute(statement).all()

        """
        Adding a user
        """
        user1 = User(name="user1")
        session.add(user1)
        session.commit()  # commit as you go like this, or use a begin context manager.

        """
        Add all of these
        """
        session.add_all([User(), User(), User()])

        """
        Delete objects
        """
        user1 = User()
        # The object is moved into the session's deleted collection until it is "flushed".
        # It is deleted when it is flushed.
        # And made permanent on commit.
        session.delete(user1)

        """
        Get by PK
        """
        my_user = session.get(User, 5)  # 5 is PK
        # You can specify composite keys using optional arguments.


if __name__ == "__main__":
    run()
