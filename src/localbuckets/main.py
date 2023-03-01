from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from . import model, api
from .database import app_config_path


app = FastAPI()
app.include_router(api.router)
app.mount('/public', StaticFiles(directory='src/public'), name='public')

print(app_config_path)


@app.get('/')
def homepage():
    return RedirectResponse('/public/index.html')
