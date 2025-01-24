from fastapi import FastAPI
from app.authors.router import router as router_authors


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "This is a main page!"}


app.include_router(router_authors)
