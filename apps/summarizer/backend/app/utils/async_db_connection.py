"""Create Asynchronous Connection with Postgres"""
from datetime import datetime as dt
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Text, DateTime

from backend.app.utils.config import ASYNC_DATABASE_URL


# Create the SQLAlchemy engine
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()


class WikiSummary(Base):
    """
    Represents the wiki_summaries table in the database.

    Attributes:
        uuid (str): The unique identifier for each summary.
        url (str): The URL of the Wikipedia page.
        summary (str): The summary text of the Wikipedia page.
        creation_date (datetime): The date and time when the summary
                                  was created.
    """
    __tablename__ = 'wiki_summaries'
    uuid = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    creation_date = Column(DateTime,
                           default=dt.now(tz=None))


async def init_db():
    """
    Initializes the database by creating the wiki_summaries table.

    This function should be called at the start of the application to ensure
    the database schema is created.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Create a session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def insert_wiki_summary(uuid, url, summary) -> str:
    """
    Inserts a new record into the wiki_summaries table.

    Args:
        uuid (str): The unique identifier for the summary.
        url (str): The URL of the Wikipedia page.
        summary (str): The summary text of the Wikipedia page.

    Returns:
        str: A message indicating whether the data was inserted successfully
             or an error occurred.
    """
    async with async_session() as session:
        async with session.begin():
            try:
                # Create a new WikiSummary object
                new_summary = WikiSummary(
                    uuid=uuid,
                    url=url,
                    summary=summary
                )

                # Add the new object to the session
                session.add(new_summary)

                # Commit the transaction
                await session.commit()

                info = "Data inserted successfully"

                return info

            except Exception as e:
                await session.rollback()
                info = f"An error occurred: {e}"
                return info


async def get_wiki_summary(u_id) -> str | None:
    """
    Retrieves the summary text for a given UUID from the wiki_summaries table.

    Args:
        u_id (str): The unique identifier for the summary.

    Returns:
        str or None: The summary text if found, otherwise None.
    """
    async with async_session() as session:
        async with session.begin():
            try:
                # Query the WikiSummary object by u_id
                result = await session.get(WikiSummary, u_id)
                if result:
                    return result.summary
                else:
                    return None
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
