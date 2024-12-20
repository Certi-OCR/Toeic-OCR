from typing import List
from fastapi import APIRouter
from automapper import mapper

from app.common.response import SuccessResponse
from app.models.history import History
from app.schemas.history import HistoryOut
from app.services.history import list_history


router = APIRouter()


@router.post("/", response_model=SuccessResponse[HistoryOut], status_code=200)
async def get_list_history():
    entities = await list_history()
    dtos = mapper.to(List[HistoryOut]).map(entities)
    return SuccessResponse(
        data=dtos,
        status_code=200,
        message="Get histories successfully",
    )
