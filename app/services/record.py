from ast import Set
from typing import List
from app.common.error import NotFound
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate
from automapper import mapper


async def create_record(record: RecordCreate):
    record_dict = mapper.to(Record).map(record)
    return await Record.insert_one(record_dict)


async def update_record(id: str, record: RecordUpdate):
    record_entity = await Record.get(id)
    if record_entity is None:
        raise NotFound("Record not found")
    record_entity.name = record.name
    record_entity.id_number = record.id_number
    record_entity.date_of_birth = record.date_of_birth
    record_entity.test_date = record.test_date
    record_entity.valid_until = record.valid_until
    record_entity.lis_score = record.lis_score
    record_entity.read_score = record.read_score
    await record_entity.save()


async def list_record() -> List[Record] | None:
    return await Record.find().to_list()


async def details_record(id: str):
    record_entity = await Record.get(id)
    if record_entity is None:
        raise NotFound("Record not found")
    return record_entity


async def delete_record(id: str):
    record_entity = await Record.get(id)
    if record_entity is None:
        raise NotFound("Record not found")
    await record_entity.delete()
