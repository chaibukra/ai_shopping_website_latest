from typing import Optional, List
from model.user import User
from repository.database import database

TABLE_NAME = "users"


async def create_user(user: User):
    query = f"""
        INSERT INTO {TABLE_NAME} (id, first_name, last_name, gender, age, email, phone, address, username, hashed_password, role)
        VALUES (:id, :first_name, :last_name, :gender, :age,:email, :phone, :address, :username, :hashed_password, :role)
    """
    user_dict = user.dict()
    user_dict["gender"] = user_dict["gender"].value
    user_dict["role"] = user_dict["role"].value
    values = {**user_dict}
    await database.execute(query, values)


async def get_by_username(username: str) -> Optional[User]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE username=:username"
    result = await database.fetch_one(query, values={"username": username})
    if result:
        return User(**result)
    else:
        return None


async def delete_user(user: User):
    query = f"""
    DELETE FROM {TABLE_NAME}
    WHERE id = :user_id
    """
    await database.execute(query, values={"user_id": user.id})


async def get_by_user_id(user_id: int) -> Optional[User]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE id =:user_id"
    result = await database.fetch_one(query, values={"user_id": user_id})
    if result:
        return User(**result)
    else:
        return None


async def get_all_users() -> Optional[List[User]]:
    query = f"SELECT * FROM {TABLE_NAME}"
    result = await database.fetch_all(query)
    if result:

        return [User(**user) for user in result]
    else:
        return None
