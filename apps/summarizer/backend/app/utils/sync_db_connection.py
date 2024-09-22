"""All custom functions used in this app"""
import datetime

from datetime import datetime as dt
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.app.utils.config import SYNC_DATABASE_URL


# Create the SQLAlchemy engine
engine = create_engine(SYNC_DATABASE_URL)

# Create a base class for declarative class definitions
Base = declarative_base()


class WikiSummary(Base):
    """
    Represents the wiki_summaries table in the database.

    Attributes:
        uuid (str): The unique identifier for each summary.
        url (str): The URL of the Wikipedia page.
        summary (str): The summary text of the Wikipedia page.
        creation_date (datetime): The date and time when the
                                  summary was created.
    """
    __tablename__ = 'wiki_summaries'
    uuid = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    creation_date = Column(DateTime,
                           default=dt.now(datetime.timezone.utc))


# Create the table in the database
Base.metadata.create_all(engine)


# Create a session factory
session_constructor = sessionmaker(bind=engine)
session = session_constructor()


def insert_wiki_summary(uuid, url, summary) -> str:
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
        session.commit()

        info = "Data inserted successfully!"

        return info

    except Exception as e:
        info = f"An error occurred: {e}"
        session.rollback()
        return info
    finally:
        # Close the session
        session.close()


def get_wiki_summary_sync(u_id) -> str | None:
    """
    Retrieves the summary text for a given UUID from the wiki_summaries table.

    Args:
        u_id (str): The unique identifier for the summary.

    Returns:
        str or None: The summary text if found, otherwise None.
    """
    try:
        # Query the WikiSummary object by uuid
        result = session.query(WikiSummary).filter_by(uuid=u_id).first()
        if result:
            return result.summary
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
