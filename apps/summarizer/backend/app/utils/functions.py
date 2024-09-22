"""All custom functions used in this app"""
import re
from typing import List

from langchain_core.documents import Document

from backend.app.build.models import ENCODING


def length_function(documents: List[Document]) -> int:
    """
    Calculate the total number of tokens for the content of the provided
    documents.

    Args:
        documents (List[Document]): A list of Document objects.

    Returns:
        int: The total number of tokens for the content of the documents.
    """
    return sum(len(ENCODING.encode(doc.page_content)) for doc in documents)


def validate_wikipedia_url(wikipedia_url: str) -> str:
    """
    Validate the format of a Wikipedia URL.

    Args:
        wikipedia_url (str): The Wikipedia URL to validate.

    Returns:
        str: A message indicating whether the URL is valid or not.
    """
    # Define the regex pattern for the Wikipedia URL
    pattern = r'^https://[a-z]{2,}\.wikipedia\.org/wiki/[\w-]+$'
    # Check if the URL matches the pattern
    if re.match(pattern, wikipedia_url):
        return "Valid Wikipedia URL"
    else:
        return "Error: Invalid Wikipedia URL format"
