from app.models.history import History
from app.schemas.history import HistoryCreate
from automapper import mapper


async def list_history():
    return await History.find_all().to_list()


async def create_history(history: HistoryCreate):
    history_dict = mapper.to(History).map(history)
    return await History.insert(history_dict)
