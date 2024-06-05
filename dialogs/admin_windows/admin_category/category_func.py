# Создание категории
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import Message
from data_base.db_config import session
from data_base.requests.category_requests import create_category, delete_category, update_category
from dialogs.admin_windows.admin_states import CategoryStates


async def new_category(message: Message,
                       widget: MessageInput,
                       dialog_manager: DialogManager,
                       ):
    category = await create_category(session, message.text.strip())
    await message.answer(text=f"{category}")
    await dialog_manager.back()


# Удаление категории
async def remove_category(callback: CallbackQuery, button: Button,
                          dialog_manager: DialogManager):
    category = dialog_manager.dialog_data["item"]
    delete = await delete_category(session, category)
    await callback.answer(delete)


# Переименовать категорию
async def new_name_category(message: Message,
                            widget: MessageInput,
                            dialog_manager: DialogManager,
                            ):
    update = await update_category(session, name=dialog_manager.dialog_data["item"],
                                   new_name=message.text)
    await message.answer(update)
    await dialog_manager.switch_to(state=CategoryStates.category_state)
