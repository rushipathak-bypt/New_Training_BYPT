from contextlib import contextmanager


@contextmanager
def db_connection():
    print("DB connected")
    conn = "connection object"

    try:
        yield conn
    finally:
        print("DB closed")


with db_connection() as db:
    print("Using DB: ", db)
