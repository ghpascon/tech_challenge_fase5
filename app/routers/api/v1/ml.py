from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fiap.utils.path import get_prefix_from_path
from app.services import ml_manager
from app.schemas.ml import PredictSchema

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


@router.get(
	'/get_model_info',
	summary='Get information about the loaded ML model',
)
async def get_model_info():
	if ml_manager.model is None:
		return JSONResponse(content={'error': 'No model loaded'}, status_code=500)

	model = ml_manager.model
	scaler = ml_manager.scaler
	features = ml_manager.feature_names
	institutions_data = ml_manager.institutions_data

	model_info = {
		'model_type': type(model).__name__,
		'scaler_type': type(scaler).__name__ if scaler else None,
		'feature_names': features if features else None,
		'institutions_data': institutions_data if institutions_data else None,
	}

	return JSONResponse(content=model_info)


@router.post(
	'/predict',
	summary='Run a prediction using the loaded ML model',
)
async def predict(data: PredictSchema):
	try:
		result = ml_manager.predict(data)
	except RuntimeError as e:
		return JSONResponse(content={'error': str(e)}, status_code=500)
	except Exception as e:
		return JSONResponse(content={'error': f'Prediction failed: {e}'}, status_code=500)

	return JSONResponse(content={'prediction': result})
