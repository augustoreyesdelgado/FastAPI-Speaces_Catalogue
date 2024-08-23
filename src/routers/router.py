from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from ..module.mapa_de_atencion import clasifica
from PIL import Image
from pydantic import BaseModel

router = APIRouter(
    prefix='/catalogo',
    tags=['catalogo']
)

templates = Jinja2Templates(directory="src/templates")

class newRequest(BaseModel):
    bandera: str 

### Endpoint ###
@router.post('/clasifica')
async def clasificar(imagen: UploadFile = File(...)):
    print('entró a clasifica')
    try:
        image = Image.open(imagen.file)
        resultado = await clasifica(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al clasificar la imagen: {e}")


    return resultado

### PAGINAS ###

@router.get('/home-page')
async def render_login_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@router.get('/results-page')
async def render_login_page(request: Request):
    return templates.TemplateResponse('results.html', {'request': request})


