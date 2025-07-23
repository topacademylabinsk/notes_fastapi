import json
import os

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, Request, responses
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

            jwt_key = jwt.encode(payload={"data": "test_payload"}, key=test_jwk)
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
        if jwt.decode(request.cookies["jwt"], test_jwk):
            return templates.TemplateResponse(request=request, name="create_note.html")
        else:
            return responses.HTMLResponse("Неправильные куки")
    except Exception:
        return responses.HTMLResponse("Неправильные куки")


@app.get("/notes")
async def get_notes(request: Request):
    return templates.TemplateResponse(request=request, name="notes.html")
