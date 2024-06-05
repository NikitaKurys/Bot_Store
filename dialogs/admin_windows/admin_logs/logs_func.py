from aiogram.types import CallbackQuery, FSInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from dialogs.admin_windows.admin_states import AdminLogsStates


# Отправить логи покупок
async def get_buy_logs(callback: CallbackQuery, select: Select,
                       dialog_manager: DialogManager, item_id: str):
    await callback.message.answer_document(FSInputFile(f'user_logs/buy_logs/{item_id}',
                                                       filename=f"{item_id}"))
    await callback.message.delete()
    await dialog_manager.start(state=AdminLogsStates.logs_state)


# Отправить логи сабскрайберов
async def get_subscribers_logs(callback: CallbackQuery, select: Select,
                               dialog_manager: DialogManager, item_id: str):
    await callback.message.answer_document(FSInputFile(f'user_logs/subscribers_logs/{item_id}',
                                                       filename=f"{item_id}"))
    await callback.answer('Файл с логами отправлен!')
    await callback.message.delete()
    await dialog_manager.start(state=AdminLogsStates.logs_state)
