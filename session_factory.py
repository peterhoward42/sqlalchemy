from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
This module shows how a singleton, module-scop session factory can be bound
to singleton, module-scope engine.

Then other modules can import and use the factory (Session variable) as shown below.

Being a factory it can be called from functions that may be running in different threads safely.
"""


# Singleton engine.
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# Singleton session factory - bound to the singleton engine.
Session = sessionmaker(engine)


def run():
    """
    Note how a context managed session can now be created, without needing access
    to the engine.

    Presumably, the block below could live in any module that imported Session from
    this module.
    """
    with Session() as session:
        session.add(None)
        session.add(None)
        session.commit()
        # closes the session

    """
    The begin() variant, that auto commits or rolls back
    """
    with Session.begin() as session:
        session.add(None)
        session.add(None)


if __name__ == "__main__":
    run()
