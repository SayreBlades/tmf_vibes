import logging
import base64
from fastapi import HTTPException, Depends, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from core_platform.config import get_app_config

security = HTTPBasic()

def authenticate(request: Request) -> str:
    config = get_app_config()
    credentials = security().__call__(request)
    
    valid_creds = False
    for cred in config.auth['credentials']:
        if cred.username == credentials.username and cred.password == credentials.password:
            valid_creds = True
            break
            
    if not valid_creds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
        
    return credentials.username
