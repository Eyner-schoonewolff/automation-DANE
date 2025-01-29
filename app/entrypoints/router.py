from fastapi.params import Param
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
    email: str = Param(..., title="Email", description="Email para enviar el reporte"),
    api_key: str = Depends(validate_api_key),
    __service: handler.ServiceAutomation = Depends(get_service),
):
    try:
        file_path = __service.process_generate_excel(
            url=os.getenv("URL_PAGE_DANE"),
        )

        report_excel = __service.process_excel(file_path)
        __service.process_email(report_excel, email)


        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "ok"},
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
