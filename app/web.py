from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates("./app/templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
