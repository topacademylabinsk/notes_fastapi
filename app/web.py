import json

from fastapi import FastAPI, Request, responses
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates("./app/templates")
app.mount("/styles", StaticFiles(directory="./app/static/styles"), name="styles")
app.mount("/images", StaticFiles(directory="./app/static/images"), name="images")


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
    test_login = "admin"
    test_password = "password"

    body = await request.body()
    data = json.loads(body)

    if data["login"] == test_login:
        if data["password"] == test_password:
            response = responses.Response(headers={"HX-Redirect": "/notes"})
            response.set_cookie("test", "test")
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
        if request.cookies["test"] == "test":
            return templates.TemplateResponse(request=request, name="create_note.html")
        else:
            return responses.HTMLResponse("Неправильные куки")
    except Exception:
        return responses.HTMLResponse("Неправильные куки")


@app.get("/notes")
async def get_notes(request: Request):
    return templates.TemplateResponse(request=request, name="notes.html")
