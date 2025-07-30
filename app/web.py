import datetime
import json
import os

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, Request, responses
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.db import DB

load_dotenv()

app = FastAPI()
templates = Jinja2Templates("./app/templates")
app.mount("/styles", StaticFiles(directory="./app/static/styles"), name="styles")
app.mount("/images", StaticFiles(directory="./app/static/images"), name="images")


test_jwk = "92379823hfjklsdbkhvglwdjkbn"


@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/auth")
async def get_auth(request: Request):
    return templates.TemplateResponse(
        status_code=302, request=request, name="auth.html"
    )


@app.post("/auth")
async def post_auth(request: Request):
    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    body = await request.body()
    data = json.loads(body)

    if data["login"] == ADMIN_LOGIN:
        if data["password"] == ADMIN_PASSWORD:
            response = responses.Response(headers={"HX-Redirect": "/notes"})

            jwt_key = jwt.encode(
                payload={
                    "user_id": "123",
                    "exp": datetime.datetime.utcnow()
                    + datetime.timedelta(minutes=1440),
                },
                key=test_jwk,
                algorithm="HS256",
            )
            response.set_cookie("jwt", jwt_key)
        else:
            response = templates.TemplateResponse(
                request=request, name="password_error.html"
            )
    else:
        response = templates.TemplateResponse(request=request, name="login_error.html")
    return response


@app.get("/create_note")
async def get_create_note(request: Request):
    try:
        if jwt.decode(
            jwt=str(request.cookies.get("jwt")), key=test_jwk, algorithms=["HS256"]
        ):
            return templates.TemplateResponse(request=request, name="create_note.html")
        else:
            return responses.HTMLResponse("Неправильные куки1")
    except Exception:
        return responses.HTMLResponse("Неправильные куки2")


class AppNote(BaseModel):
    title: str
    description: str


@app.post("/create_note")
async def create_note(request: Request, data: AppNote):
    db = DB("test_db.db3")
    db.create_note(data.title, data.description)


@app.get("/notes")
async def get_notes(request: Request):
    return templates.TemplateResponse(request=request, name="notes.html")
