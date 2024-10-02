# save this as app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates 

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    title = "Hello from FastAPI"
    message = "Hello World !"
    return templates.TemplateResponse("index.html", {"request": request, "title": title, "message": message})
