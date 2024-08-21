from fastapi import FastAPI, Request, status
from src.routers import router

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), name='static')

@app.get('/')
def test(request: Request):
    return RedirectResponse(url="/catalogo/home-page", status_code=status.HTTP_302_FOUND)

@app.get('/healthy')
async def health_check():
    return {'status': 'Healthy'}

app.include_router(router.router)