from fastapi import APIRouter, Depends, HTTPException, status
from app.services import handler
from fastapi.responses import JSONResponse
from app.entrypoints.dependencies import validate_api_key, get_service
import os

automation = APIRouter()


@automation.post(
    "/automation",
    response_model=[],
    status_code=status.HTTP_200_OK,
    tags=["automation"],
    description="Endpoint para procesar la automatización de la descarga de archivos",
    dependencies=[Depends(validate_api_key), Depends(get_service)],
)
def processing_analysis(
    api_key: str = Depends(validate_api_key),
    service_: handler.ServiceAutomatication = Depends(get_service),
):
    try:
        automation = service_.process_generate_excel(
            url=os.getenv("URL_PAGE_DANE"),
        )
        JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Archivo generado con éxito", "file_path": automation},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )
