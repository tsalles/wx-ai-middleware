import os

from fastapi import APIRouter, HTTPException, Depends

from app.models import GenerateRequest, GenerateResponse
from app.models import GenerateRequestSimple, GenerateResponseSimple

from app.auth import get_api_key

import json
from ibm_watsonx_ai.foundation_models import ModelInference

from dotenv import load_dotenv

import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

router = APIRouter()

wx_ai_credentials = {
    "url": os.getenv("WATSONX_URL"),
    "apikey": os.getenv("WATSONX_APIKEY"),
}

model_id = os.getenv("WATSONX_MODEL")
project_id = os.getenv("WATSONX_PROJECT_ID")
space_id = os.getenv("WATSONX_SPACE_ID")
verify = False

model = ModelInference(
    model_id=model_id,
    credentials=wx_ai_credentials,
    project_id=project_id,
    space_id=space_id,
    verify=verify,
)


@router.post(
    "/generate_text",
    response_model=GenerateResponse,
    dependencies=[Depends(get_api_key)],
    summary="Generates Text using generative AI",
    description="Generates text using watsonx.ai service.",
    operation_id="generate_text_generate_post",
    tags=["genai"],
)
def generate_text(request: GenerateRequest) -> GenerateResponse:
    params = request.parameters.dict(exclude_none=True) if request.parameters else {}
    try:
        return model.generate(prompt=request.input, params=params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/generate",
    response_model=GenerateResponseSimple,
    dependencies=[Depends(get_api_key)],
    summary="[Simple] Generates Text using generative AI",
    description="[Simple] Generates text using a simplified API from watsonx.ai service.",
    operation_id="generate_text_simple_generate_post",
    tags=["genai"],
)
def generate(request: GenerateRequestSimple) -> GenerateResponseSimple:
    params = {
        'decoding_method': request.decoding_method,
        'temperature': request.temperature,
        'top_p': request.top_p,
        'top_k': request.top_k,
        'min_new_tokens': request.min_new_tokens,
        'max_new_tokens': request.max_new_tokens,
        'stop_sequences': request.stop_sequences,
        'project_id': request.project_id,
        'model_id': request.model_id
    }
    try:
        data = '\n'.join([r['generated_text'].strip()
                          for r in model.generate(prompt=request.input, params=params)['results']])
        return GenerateResponseSimple(
            generated_text=data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
