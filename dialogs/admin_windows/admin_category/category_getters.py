from aiogram_dialog import DialogManager

from data_base.db_config import session
from data_base.requests.category_requests import get_categories


async def show_categories(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.dialog_data.get('is_checked')
    categories = []
    for category in await get_categories(session):
        categories.append((category.name, len(category.products), category.products))
    return {"categories": categories,
            "checked": checked,
            "not_checked": not checked}
