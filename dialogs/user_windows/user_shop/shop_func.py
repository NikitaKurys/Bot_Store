from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button, ManagedMultiselect
from dialogs.user_windows.user_states import ShopStates


# Обработка чекбокса
async def select_clicked(callback: CallbackQuery, checkbox: ManagedMultiselect,
                         dialog_manager: DialogManager, item: str) -> None:
    dialog_manager.dialog_data.update(item=item, clicked=checkbox.is_checked(item))
    # Если ничего не выбрано - сбрасываем выделения
    if len(checkbox.get_checked()) == 0:
        del dialog_manager.dialog_data['item']


# Перейти к продуктам
async def show_products(callback: CallbackQuery, widget: Select,
                        dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(user_id=callback.from_user.id, category=item_id)
    category = dialog_manager.dialog_data.get('category').lower()
    if category == 'духи' or category == 'масло':
        await dialog_manager.switch_to(state=ShopStates.gender_states)
    else:
        await dialog_manager.next()


# Переход между категориями
async def switch_to_categories(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=ShopStates.category_states)
    dialog_manager.dialog_data.clear()
    await dialog_manager.find('stub_scroll').set_page(0)
    await dialog_manager.find("price").reset_checked()
    await dialog_manager.find("checkbox").set_checked(True)


# Сортировка по гендеру
async def sort_gender(callback: CallbackQuery, widget: Select,
                      dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(gender=item_id)
    await dialog_manager.switch_to(state=ShopStates.product_states)
    