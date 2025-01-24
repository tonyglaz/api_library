from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "This is a main page!"}