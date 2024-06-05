import os
from pathlib import Path

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select

from aiogram.types import Message, CallbackQuery

from data_base.db_config import session
from data_base.requests.product_requests import create_product, delete_product, update_product
from dialogs.admin_windows.admin_states import ProductStates


# Создание имени продукта
async def create_name_product(message: Message,
                              widget: MessageInput,
                              dialog_manager: DialogManager,
                              ):
    dialog_manager.dialog_data.update(category=dialog_manager.start_data, name=message.text, )
    await dialog_manager.next()


# Создание фото продукта
async def create_photo_product(message: Message,
                               widget: MessageInput,
                               dialog_manager: DialogManager,
                               ):
    file = message.photo[-1].file_id
    category = dialog_manager.dialog_data['category']
    destination = f"static/product_photo/{category}/{file}.png"

    if Path(f"static/product_photo/{category}").exists() is False:
        os.mkdir(f"static/product_photo/{category}")

    await message.bot.download(file=file, destination=destination)
    dialog_manager.dialog_data.update(photo=f"{destination}")
    await dialog_manager.next()


# Создание описания продукта
async def create_description_product(message: Message,
                                     widget: MessageInput,
                                     dialog_manager: DialogManager,
                                     ):
    dialog_manager.dialog_data.update(description=message.text)
    await dialog_manager.next()


# Создание цены продукта
async def create_price_product(message: Message,
                               widget: MessageInput,
                               dialog_manager: DialogManager,
                               ):
    dialog_manager.dialog_data.update(price=int(message.text))
    await dialog_manager.next()


# Выбор гендера и создание продукта
async def create_gender_product(callback: CallbackQuery, widget: Select,
                                dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(gender=item_id)
    product = dialog_manager.dialog_data
    await callback.answer(await create_product(
        session,
        name=product["name"],
        category=product["category"],
        description=product["description"],
        gender=product["gender"],
        path_to_img=product["photo"],
        price=product["price"],
    ))
    await dialog_manager.done()


# Удаление продукта
async def remove_product(callback: CallbackQuery, button: Button,
                         dialog_manager: DialogManager):
    product_id = int(dialog_manager.dialog_data["item"])
    delete = await delete_product(session, product_id, )
    await callback.answer(delete)


# Обновление имени продукта
async def update_name(message: Message,
                      widget: MessageInput,
                      dialog_manager: DialogManager,
                      ):
    await message.answer(await update_product(session, product_id=int(dialog_manager.dialog_data["item"]),
                                              product_name=message.text))
    await dialog_manager.switch_to(ProductStates.product_state)


# Обновление описания продукта
async def update_description(message: Message,
                             widget: MessageInput,
                             dialog_manager: DialogManager,
                             ):
    await message.answer(await update_product(session, product_id=int(dialog_manager.dialog_data["item"]),
                                              product_name=message.text))
    await dialog_manager.switch_to(ProductStates.product_state)


# Обновление гендера продукта
async def update_gender_product(callback: CallbackQuery, widget: Select,
                                dialog_manager: DialogManager, item_id: str):
    await callback.answer(await update_product(session, product_id=int(dialog_manager.dialog_data["item"]),
                                               product_gender=item_id))
    await dialog_manager.switch_to(ProductStates.product_state)


# Обновление цены продукта
async def update_price(message: Message,
                       widget: MessageInput,
                       dialog_manager: DialogManager,
                       ):
    await message.answer(await update_product(session, product_id=int(dialog_manager.dialog_data["item"]),
                                              product_price=message.text))
    await dialog_manager.switch_to(ProductStates.product_state)


# Обновление фото продукта
async def update_photo_product(message: Message,
                               widget: MessageInput,
                               dialog_manager: DialogManager,
                               ):
    file = message.photo[-1].file_id
    destination = f"product_photo/{file}.png"
    await message.bot.download(file=file, destination=destination)
    await message.answer(await update_product(session, product_id=int(dialog_manager.dialog_data["item"]),
                                              product_img=destination))
    await dialog_manager.switch_to(ProductStates.product_state)


# Обновление категории продукта
async def update_category_product(callback: CallbackQuery, widget: Select,
                                  dialog_manager: DialogManager, item_id: str):
    await callback.answer(await update_product(session, product_id=int(dialog_manager.dialog_data["item"]),
                                               category=item_id))
    await dialog_manager.switch_to(ProductStates.product_state)
