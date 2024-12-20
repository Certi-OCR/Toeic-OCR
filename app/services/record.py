from ast import Set
from app.common.error import NotFound
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate
from automapper import mapper


async def create_record(record: RecordCreate):
    record_dict = mapper.to(Record).map(record)
    return await Record.insert_one(record_dict)


async def update_record(id: str, record: RecordUpdate):
    record_entity = await Record.find_one(Record.id == id)
    if record_entity is None:
        raise NotFound("Record not found")
    record_set = Set(
        {
            Record.name: record.name,
            Record.id_number: record.id_number,
            Record.date_of_birth: record.date_of_birth,
            Record.test_date: record.test_date,
            Record.valid_until: record.valid_until,
            Record.lis_score: record.lis_score,
            Record.read_score: record.read_score,
        }
    )
    record_entity.update(record_set)


async def list_record():
    await Record.find_all().to_list()


async def details_record(id: str):
    record_entity = await Record.find_one(Record.id == id)
    if record_entity is None:
        raise NotFound("Record not found")
    return record_entity


async def delete_record(id: str):
    record_entity = await Record.find_one(Record.id == id)
    if record_entity is None:
        raise NotFound("Record not found")
    await record_entity.delete()
