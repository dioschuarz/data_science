"""Main file to initialize the application"""
from backend.app.api.main import app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)