import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")


class ApiKeyManager:
    KEY = secrets.token_urlsafe()

    @classmethod
    def verify(cls, api_key_header: str = Security(API_KEY_HEADER)) -> None:
        if api_key_header != cls.KEY:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
