from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message

from data_base.db_config import session
from data_base.requests.user_requests import set_admin, get_user
from dialogs.admin_windows.admin_states import AddAdminStates


# Добавить администратора
async def create_admin(message: Message,
                       widget: MessageInput,
                       dialog_manager: DialogManager,
                       ):
    if message.text.isdigit():
        if await get_user(session, int(message.text)):
            await message.answer(await set_admin(session, int(message.text)))
            await dialog_manager.switch_to(state=AddAdminStates.show_admin_state)
        else:
            await message.answer(f"Пользователь с ID {message.text} не зарегистрирован\n"
                                 f"попросите его написать нашему боту разок ^_^")
    else:
        await message.answer('Вы ввели какую-то фигню :)\n'
                             'ID должен содержать только цифры')
