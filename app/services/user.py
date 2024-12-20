from beanie import PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.common.error import NotFound
from app.core.auth.jwt import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from beanie.exceptions import DocumentNotFound


async def create_user(user: UserCreate):
    user_dict = user.model_dump()
    user_dict["hashed_password"] = get_password_hash(user.password)
    await User.insert_one(user_dict)


async def get_user_by_username(username: str) -> User:
    user = await User.find_one({"username": username})
    if user:
        return user
    return None


async def get_user_by_email(email: str) -> User:
    user = await User.find_one({"email": email})
    if user:
        return user
    return None


async def get_user_by_id(id: PydanticObjectId) -> User:
    user = await User.get(id)
    if user:
        return user
    return None


async def update_user(id: PydanticObjectId, user: UserUpdate):
    user_entity = await User.get(id)
    if user.password != None:
        user_entity.hashed_password = get_password_hash(user.password)
    if user.full_name != None:
        user_entity.full_name = user.full_name
    try:
        await user_entity.replace()
    except (ValueError, DocumentNotFound):
        raise NotFound(message="User not found")


async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
