from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException, status
from core.config import settings

api_key_header = APIKeyHeader(name='Authorization')

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    return api_key
