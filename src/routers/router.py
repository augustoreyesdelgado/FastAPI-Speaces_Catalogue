from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/catalogo',
    tags=['catalogo']
)

templates = Jinja2Templates(directory="src/templates")

### PAGES ###

@router.get('/home-page')
def render_login_page(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})
