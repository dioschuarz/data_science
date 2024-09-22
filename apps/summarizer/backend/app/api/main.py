"""FastAPI Setup."""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.app.api.routes.summarizer import summarizer_router
from backend.app.utils.async_db_connection import init_db


app = FastAPI(title="Wikipedia Summarizer API")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Define the lifespan context manager.

    This context manager initializes the database at the start of
    the application and can be used for any necessary cleanup
    when the application shuts down.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # Initialize the database
    await init_db()
    yield
    # Any cleanup can be done here if needed


app.router.lifespan_context = lifespan

app.include_router(summarizer_router, tags=["wikipedia"])


@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the Wikipedia Summarizer API!"}
