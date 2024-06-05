from data_base.models import User
from data_base.db_config import session


# Проверка на админа
async def get_admin_id(event_from_user: User, **kwargs):

    from data_base.requests.user_requests import get_user

    user = await get_user(session, event_from_user.id)
    if user:
        if user.is_admin == True:
            return {"is_admin": True}
        else:
            return {"is_admin": False}


# Получить имя
async def get_username(event_from_user: User, **kwargs):
    return {"username": event_from_user.first_name}
