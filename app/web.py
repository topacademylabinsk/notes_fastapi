from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import responses

app = FastAPI()
templates = Jinja2Templates("./app/templates")
app.mount("/styles", StaticFiles(directory="./app/static/styles"), name="styles")
app.mount("/images", StaticFiles(directory="./app/static/images"), name="images")


@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/auth")
async def get_auth(request: Request):
    return templates.TemplateResponse(status_code=302, request=request, name="auth.html")

@app.post("/auth")
async def post_auth(request: Request):
    response = responses.Response(headers={"HX-Redirect": "/notes"})
    response.set_cookie("test", "test")
    return response

@app.get("/create_note")
async def get_create_note(request: Request):
    return templates.TemplateResponse(request=request, name="create_note.html")

@app.get("/notes")
async def get_notes(request: Request):
    return templates.TemplateResponse(request=request, name="notes.html")
