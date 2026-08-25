from fastapi import Header, HTTPException, status
from .config import get_settings

settings = get_settings()


def require_admin_key(x_api_key: str | None = Header(default=None)) -> str:
    if x_api_key != settings.admin_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin API key")
    return "admin"


def require_sdk_key(x_api_key: str | None = Header(default=None)) -> str:
    if x_api_key not in {settings.sdk_api_key, settings.admin_api_key}:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid SDK API key")
    return "sdk"
