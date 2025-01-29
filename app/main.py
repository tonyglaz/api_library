from fastapi import FastAPI
from app.authors.router import router as router_authors
from app.books.router import router as router_books


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "This is a main page!"}


app.include_router(router_authors)
app.include_router(router_books)
