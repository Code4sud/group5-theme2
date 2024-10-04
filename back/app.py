from db import models
from fastapi import FastAPI, Request, Depends, Form, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from db.database import SessionLocal, engine
from db import crud, database, models, schemas
import shutil
import os

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory="templates")
app.mount("/header/images", StaticFiles(directory="templates/header/images"), name="images")

# Vérifie si le dossier uploads existe, sinon le crée
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Route pour gérer l'upload de fichier
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Vérification des types de fichiers acceptés
    if file.content_type not in ["image/jpeg"]:
        return {"error": "Format de fichier non pris en charge. Seuls les fichiers jpeg sont acceptés."}

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return {"error": "Une erreur est survenue lors de l'upload."}
    
    return {"filename": file.filename}

# Autres routes existantes...
@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/onboarding")

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

@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding(request: Request):
    image_file = "/header/images/arbre1.jpeg"
    return templates.TemplateResponse("onboarding.html", {"request": request, "image_file": image_file})