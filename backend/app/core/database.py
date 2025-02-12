from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

engine = create_engine(settings.database_url)


def create_db_and_tables() -> None:
    """Creates the database and tables defined in the SQLModel metadata.

    This function is used to initialize the database schema.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Returns a generator that yields a database session.

    The session is created using the engine defined in the settings.
    The session is yielded within a context manager,
    ensuring it is properly closed when finished.

    Yields:
        Session: A database session.
    """
    with Session(engine) as session:
        yield session
