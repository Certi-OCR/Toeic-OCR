from typing import List
from fastapi import APIRouter
from automapper import mapper

from app.common.response import SuccessResponse
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordOut, RecordUpdate
from app.services.record import (
    create_record,
    delete_record,
    details_record,
    list_record,
    update_record,
)


router = APIRouter()


@router.get("/", response_model=SuccessResponse[RecordOut], status_code=200)
async def get_list_record():
    entities = await list_record()
    dtos = mapper.to(List[RecordOut]).map(entities)
    return SuccessResponse(
        data=dtos,
        status_code=200,
        message="Get records successfully",
    )


@router.get("/{id}", response_model=SuccessResponse[RecordOut], status_code=200)
async def get_details_record(id: str):
    entity = await details_record(id)
    dto = await mapper.to(RecordOut).map(entity)
    return SuccessResponse(
        data=dto,
        status_code=200,
        message="Get records successfully",
    )


@router.post("/create")
async def add_record(record: RecordCreate):
    await create_record(record)
    return SuccessResponse(status_code=200, message="Add record successfully")


@router.put("/update/{id}")
async def update_record_by_id(id: str, record: RecordUpdate):
    await update_record(id, record)
    return SuccessResponse(status_code=200, message="Update record successfully")


@router.delete("/delete/{id}")
async def delete_record_by_id(id: str):
    await delete_record(id)
    return SuccessResponse(status_code=200, message="Delete record successfully")
