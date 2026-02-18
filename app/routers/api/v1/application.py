from app import __version__

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fiap.utils.path import get_prefix_from_path
from app.core import alerts_manager


router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


@router.get('/get_alerts', summary='Get current alerts')
async def get_alerts():
	return JSONResponse(content=alerts_manager.get_alerts())


@router.get('/get_version', summary='Get the current application version')
async def get_version():
	return JSONResponse(content={'version': __version__})
