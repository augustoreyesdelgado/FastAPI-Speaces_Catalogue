from fastapi import APIRouter, Request, File, UploadFile, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from ..module.mapa_de_atencion import clasifica
from PIL import Image
from pydantic import BaseModel
from io import BytesIO
import uuid

router = APIRouter(
    prefix='/catalogo',
    tags=['catalogo']
)

templates = Jinja2Templates(directory="src/templates")

router.mount("/static", StaticFiles(directory="src/static/temp"), name="static")

class newRequest(BaseModel):
    bandera: str 

### Endpoint ###
@router.post('/clasifica')
async def clasificar(imagen: UploadFile = File(...)):
    try:
        image = Image.open(imagen.file)
        resultado, certeza, processed_image = await clasifica(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al clasificar la imagen: {e}")

    # Guardar la imagen procesada en una ubicación temporal
    image_id = str(uuid.uuid4())
    image_path = f"src/static/temp/{image_id}.png"
    processed_image.save(image_path, format="PNG")

    # Devolver el resultado y la URL de la imagen
    return JSONResponse(content={"resultado": resultado, "certeza": certeza, "image_url": f"/static/temp/{image_id}.png"})

### PAGINAS ###

@router.get('/home-page')
async def render_login_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@router.post('/results-page')
async def render_results_page(request: Request, resultado: str = Form(...), certeza: str = Form(...), image_url: str = Form(...)):
    return templates.TemplateResponse('results.html', {
        'request': request,
        'resultado': resultado,
        'certeza': certeza,
        'image_url': image_url
    })


