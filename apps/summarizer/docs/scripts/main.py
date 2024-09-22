"""FastAPI Setup"""
import re
import uuid

from fastapi import (FastAPI,
                     HTTPException)
from pydantic import BaseModel, Field


class ArticleRequest(BaseModel):
    "Schema from Input of FastAPI"
    wikipedia_url: str = Field(
        default="https://pt.wikipedia.org/wiki/Nikola_Tesla",
        title="URL from Wikipedia article."
    )
    number_of_words: int = Field(
        default=1000,
        title="Maximum number of words desired in the final summary."
    )


def validate_wikipedia_url(wikipedia_url: str) -> str:
    "Define the regex pattern for the Wikipedia URL"
    pattern = r'^https://[a-z]{2,}\.wikipedia\.org/wiki/[\w-]+$'
    # Check if the URL matches the pattern
    if re.match(pattern, wikipedia_url):
        return "Valid Wikipedia URL"
    else:
        return "Error: Invalid Wikipedia URL format"


app = FastAPI(title="Wikipedia Summarizer API")


@app.post("/summarizer/insert_article")
def generate_id(request: ArticleRequest):
    "Function to Generate an ID."
    u_id = str(uuid.uuid4())
    response = {"id": u_id}
    url = request.wikipedia_url
    nw = request.number_of_words
    validation_result = validate_wikipedia_url(url)
    if validation_result != "Valid Wikipedia URL":
        raise HTTPException(status_code=400, detail=validation_result)
    if (nw is None) or (nw < 1000):
        nw = 1000
        response.update(
                {"warning": ("You configured the number of words "
                             "below 1000, the lowest value of "
                             "this parameter is 1000.")
                 }
            )
    else:
        response.update({"info": ("Article URL "
                                  "is valid and has been "
                                  "inserted successfully!")
                         }
                        )
    return response
