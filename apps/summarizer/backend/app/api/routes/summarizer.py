"""Routes controller."""
import uuid

from fastapi import APIRouter, HTTPException

from backend.app.utils.config import ArticleRequest
from backend.app.utils.async_db_connection import (get_wiki_summary,
                                                   insert_wiki_summary)
from backend.app.utils.functions import validate_wikipedia_url
from backend.app.build.graphs.workflow import SUMMARIZER_GRAPH
from backend.app.build.loader import load_article_content


summarizer_router = APIRouter(prefix="/summarizer")


@summarizer_router.post("/insert_article", response_model=dict)
async def insert_article(request: ArticleRequest):
    """
    Insert a Wikipedia article and generate a summary.

    This function generates a unique ID for the article, validates the URL,
    loads the article content, and invokes the summarizer graph to generate
    a summary. The summary is then inserted into the database.

    Args:
        request (ArticleRequest): The request containing the Wikipedia URL
                                  and the desired number of words.

    Returns:
        dict: A dictionary containing the unique ID and any relevant
              information or warnings.
    """
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
                         "this parameter is 1000.")}
        )
    else:
        raw_doc = load_article_content(url)
        defs = {"contents": [doc.page_content for doc in [raw_doc]],
                "token_max": nw}
        try:
            summ_text = await SUMMARIZER_GRAPH.ainvoke(defs,
                                                       {"recursion_limit": 10})
            info = await insert_wiki_summary(u_id,
                                             url,
                                             summ_text["final_summary"])
            if "error" in info:
                raise HTTPException(status_code=500, detail=info)
            response.update({"info": info, "id": u_id})
        except Exception as e:
            raise HTTPException(status_code=500, detail=e) from e
    return response


@summarizer_router.get("/get_summary/{uuid}")
async def get_summary(u_id: str):
    """
    Retrieve a summary by UUID.

    This function fetches the summary associated with the given UUID from
    the database.

    Args:
        u_id (str): The unique identifier for the summary.

    Returns:
        dict: A dictionary containing the UUID and the summary text, if found.
    """
    try:
        summary = await get_wiki_summary(u_id)
        if summary:
            return {"uuid": u_id, "summary": summary}
        else:
            raise HTTPException(status_code=404, detail="Summary not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
