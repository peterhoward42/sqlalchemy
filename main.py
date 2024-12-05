from sqlalchemy import create_engine, text


def run():

    # A function-scoped engine that points to an in memory database.
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    """
    The <connect> context manager closes the connection when it exits.
    Neither the code block nor the <connect> context manager does a database commit,
    so the stdout will show the engine doing a rollback.
    """
    with engine.connect() as conn:
        # Uses low-level direct SQL text execution.
        result = conn.execute(text("select 'hello world'"))
        print(result.all())

    """ 
    This time the code block does a commit.
    """
    with engine.connect() as conn:
        # Shows the direct way of executing DDL and a row insertion.
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()

    """
    engine.begin() is a context manager that auto commits.
    
    PREFER THIS STYLE in real code.
    
    Or does a rollback if there is an exception.
    """
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
        )

    """
    Selecting from a table.
    Type of result is CursorResult.
    
    The returned rows are named-tuples.
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"x: {row.x}  y: {row.y}")

    """
    Demonstrating a WHERE clause.
    """
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2}
        )
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


if __name__ == "__main__":
    run()
