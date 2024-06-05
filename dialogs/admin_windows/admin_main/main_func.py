from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedMultiselect, Select

from dialogs.admin_windows.admin_states import ProductStates
from aiogram.types import CallbackQuery


# Изменение состояния чекбокса
async def checkbox_clicked(callback: CallbackQuery, checkbox: ManagedMultiselect,
                           dialog_manager: DialogManager, item: str, ) -> None:
    dialog_manager.dialog_data.update(is_checked=checkbox.is_checked(item), item=item)


# Удаление состояния чекбокса после изменения элемента
async def reset_checked(callback: CallbackQuery, checkbox: ManagedMultiselect,
                        dialog_manager: DialogManager, item: str, ) -> None:
    checked_item = checkbox.get_checked()
    if len(checked_item) != 0:
        if checked_item[0] not in callback.data:
            dialog_manager.dialog_data.clear()
            await checkbox.reset_checked()


# Переключиться в диалог продуктов
async def switch_to_products(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    await dialog_manager.start(state=ProductStates.product_state, data=item_id)

