from db import models
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates 
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from db.database import SessionLocal, engine
from db import crud , database, models, schemas
import os 
from perplexipy import PerplexityClient

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



templates = Jinja2Templates(directory="templates")
# Monte le répertoire 'templates/header/images' en tant que source de fichiers statiques
# à l'URL '/header/images'.
# Cela permet d'accéder aux fichiers situés dans ce répertoire via une URL,
# par exemple, pour récupérer une image, on peut utiliser : 
# http://localhost:8000/header/images/nom_de_l_image.ext
#  
app.mount("/header/images", StaticFiles(directory="templates/header/images"), name="images")


@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/onboarding")

# page de recherche
@app.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@app.get("/result", response_class=HTMLResponse)
async def result(request: Request):

    image_file3 = "/header/images/avant.jpg"  
    image_file4 = "/header/images/apres.jpg"  

    return templates.TemplateResponse("result.html", {"request": request, "image_file1": image_file3,"image_file2": image_file4})


@app.get("/example", response_class=HTMLResponse)
async def example(request: Request):
    return templates.TemplateResponse("example.html", {"request": request})


key = "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"
client = PerplexityClient(key = key)


@app.post("/openai")
async def query_openai(
    name: str = Form(...), 
    city: str = Form(...), 
    prompt: str = Form(...)):
    if not key:
        raise HTTPException(status_code=500, detail="OpenAI API key is not configured.")
    
    try:
        result = client.query('what is the climate of that location : grand rue, Strasbourg 67000. tell me 3 types of trees we can find in that region. anwser should only be a json file with the keys :  climate (str) et treeList (list str)' )
        print(result)
        return client.query('what is the climate of that location : grand rue, Strasbourg 67000. tell me 3 types of trees we can find in that region. anwser should only be a json file with the keys :  climate (str) et treeList (list str)' )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_simple_user")
def create_simple_user(
    name: str = Form(...), 
    city: str = Form(...), 
    db: Session = Depends(get_db)):

    user = crud.create_simpleuser(db, name=name, city=city)
    print(user.city, user.name, user.id)
    return RedirectResponse(url="/search", status_code=303)

# @app.get("/get-picture")
# def get_picture(

# )

@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding(request: Request):
    # Définition des chemins d'accès aux images
    image_file3 = "/header/images/arbre-new-1.jpg"  
    image_file4 = "/header/images/arbre-new-2.jpg"  

    # Retourne une réponse au format HTML en utilisant le template 'onboarding.html'.
    # On passe un dictionnaire contenant l'objet 'request' (qui représente la requête HTTP actuelle)
    # et les chemins des deux images afin qu'ils soient accessibles dans le template.
    return templates.TemplateResponse("onboarding.html", {
        "request": request,
        "image_file1": image_file3,
        "image_file2": image_file4
    })