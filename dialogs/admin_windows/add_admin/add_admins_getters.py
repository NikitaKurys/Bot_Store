from aiogram_dialog import DialogManager

from data_base.db_config import session
from data_base.requests.user_requests import get_all_admins


# Получить всех админов
async def show_admins(dialog_manager: DialogManager, **kwargs):
    users = []
    for user in await get_all_admins(session):
        users.append(
            (
                user.id,
                user.first_name
            )
        )
    return {
            "admins": users
            }
