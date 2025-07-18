from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates("./app/templates")
app.mount("/styles", StaticFiles(directory="./app/static/styles"), name="styles")
app.mount("/images", StaticFiles(directory="./app/static/images"), name="images")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
