from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCheckbox, ManagedMultiselect


# Изменение состояния чекбокса
async def checkbox_clicked(callback: CallbackQuery, checkbox: ManagedCheckbox,
                           dialog_manager: DialogManager,) -> None:
    dialog_manager.dialog_data.update(is_checked=checkbox.is_checked())


# Удаление состояния чекбокса
async def reset_checkbox_clicked(callback: CallbackQuery, checkbox: ManagedMultiselect,
                                 dialog_manager: DialogManager, item: str) -> None:
    if dialog_manager.dialog_data.get('clicked') is True and checkbox.is_checked(item) is False:
        await checkbox.reset_checked()

