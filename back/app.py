from db import models
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates 
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db import crud , database, models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/onboarding")

@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@app.get("/result", response_class=HTMLResponse)
async def result(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})


@app.get("/example", response_class=HTMLResponse)
async def example(request: Request):
    return templates.TemplateResponse("example.html", {"request": request})

@app.post("/create_simple_user")
def create_simple_user(
    name: str = Form(...), 
    city: str = Form(...), 
    db: Session = Depends(get_db)):

    user = crud.create_simpleuser(db, name=name, city=city)
    print(user.city, user.name, user.id)
    return RedirectResponse(url="/search", status_code=303)
