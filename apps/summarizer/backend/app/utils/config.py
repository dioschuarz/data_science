"""Load variables and classes used in this app"""
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field


load_dotenv()


class ArticleRequest(BaseModel):
    """
    Schema for the input of FastAPI.

    Attributes:
        wikipedia_url (str): The URL of the Wikipedia article.
        number_of_words (int): The maximum number of words desired in the
        final summary.
    """
    wikipedia_url: str = Field(
        default="https://pt.wikipedia.org/wiki/Nikola_Tesla",
        title="URL of the Wikipedia article."
    )
    number_of_words: int = Field(
        default=1000,
        title="Maximum number of words desired in the final summary."
    )


# Database connection URLs
SYNC_DATABASE_URL = "postgresql" + os.getenv("POSTGRES_DB_URL")
ASYNC_DATABASE_URL = "postgresql+asyncpg" + os.getenv("POSTGRES_DB_URL")

# Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
