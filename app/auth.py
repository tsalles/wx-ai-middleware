import os
from fastapi import HTTPException, Header
from dotenv import load_dotenv

load_dotenv()


def get_api_key(x_api_key: str = Header(None)):
    if x_api_key != os.getenv('WATSONX_APIKEY'):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


