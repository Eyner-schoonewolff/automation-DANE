from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

from app.adapters import localization_web_process, process_file
from app.services import handler

load_dotenv()

secret_key = os.environ.get("API_KEY_HEADER")
api_key_header = APIKeyHeader(name="api_key_header", description="api key propital")


def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key_header:
        if secret_key == api_key:
            return api_key_header
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalidate api key"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="api key not found"
        )


def get_repo():
    return localization_web_process.DANEAdapter(), process_file.AdapterExcel()

def get_service(
    repo: tuple = Depends(get_repo)
):
    repo_instance, processor_instance = repo
    return handler.ServiceAutomatication(repo=repo_instance, processor=processor_instance)

