import os
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
API_KEY = os.getenv("API_KEY")
API_KEY_HEADER = os.getenv("API_KEY_HEADER")
api_key_header = APIKeyHeader(name=API_KEY_HEADER)

def get_current_user(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail = "Invalid API Key")
    return {"username": "authenticated_user"}
