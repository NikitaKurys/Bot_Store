from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from aiogram import Router, F

from dialogs.user_windows.user_states import ShopStates

router = Router()


@router.callback_query(F.data == 'check_news')
async def process_start(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=ShopStates.category_states, mode=StartMode.RESET_STACK)

