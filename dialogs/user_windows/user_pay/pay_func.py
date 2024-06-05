from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram import types
from data_base.db_config import config
from parser.parser import get_delivery_price


# Перейти к локации
async def go_to_location(callback: CallbackQuery, widget: Select,
                         dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(location=item_id)
    await dialog_manager.next()


# Добавить локацию
async def create_location(message: Message,
                          widget: MessageInput,
                          dialog_manager: DialogManager,
                          ):
    if dialog_manager.dialog_data.get('location') == 'Почта России 📪':
        if message.text.isdigit() and len(message.text) == 6:
            await message.answer(
                f"Секундочку, ищем адрес по индексу...."
            )
            parser = await get_delivery_price(message.text.replace(" ", ""))
            if type(parser) is dict:
                await message.answer(
                    f"Ваш индекс {message.text} принят\n{parser['location']}"
                )
                dialog_manager.dialog_data.update(location=parser["location"], delivery_price=parser['price'])
                await dialog_manager.next()
            else:
                await message.answer(
                    f"{parser}, укажите почтовый индекс России"
                )

        else:
            await message.answer(
                f"{message.text} - не подходит под формат индекса"
            )
    else:
        await message.answer(
            f"Ваш адрес {message.text} принят"
        )
        dialog_manager.dialog_data.update(location=message.text)
        await dialog_manager.next()


# Добавить контакт
async def create_contact(message: Message,
                         widget: MessageInput,
                         dialog_manager: DialogManager,
                         ):
    number = message.text.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
    if len(number) == 11 and number.isdigit():
        await message.answer(
            f"Ваш номер телефона {number} принят"
        )
        dialog_manager.dialog_data.update(contact=number)
        await dialog_manager.next()
    else:
        await message.answer(
            f"Не подходящий формат номера телефона!\n"
            f"Введите 8-XXX-XXX-XX-XX",
        )


# Оплата
async def go_to_puy(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if config.tg_bot.pay_token.split(':')[1] == 'TEST':
        await callback.bot.send_message(callback.message.chat.id, "Тестовый платеж!!!")
    products = []
    for product in dialog_manager.start_data[0]:
        if product.get('value'):
            products.append(types.LabeledPrice(label=f"{product['category']} {product['name']} {product['value']}",
                                               amount=int(product['price']) * 100))
        else:
            products.append(types.LabeledPrice(label=f"{product['category']} {product['name']}",
                                               amount=int(product['price']) * 100))
    if dialog_manager.dialog_data.get('delivery_price') is not None:
        products.append(types.LabeledPrice(label='Доставка', amount=dialog_manager.dialog_data['delivery_price'] * 100))

    await callback.bot.send_invoice(callback.message.chat.id,
                                    title="Покупка ароматов",
                                    description=f"{dialog_manager.dialog_data['location']}",
                                    provider_token=config.tg_bot.pay_token,
                                    currency="rub",
                                    photo_url="https://sun9-25.userapi.com/impg/hrm8IcOaT52aztpQCsw8q29wQ9tT76Lyx80BIg"
                                              "/5TxAs2YvLIo.jpg?size=1238x1240&quality=95&sign=3ccc03b6e984034ab71d79f4"
                                              "33ba447c&type=album",
                                    photo_width=416,
                                    photo_height=234,
                                    photo_size=416,
                                    is_flexible=False,
                                    prices=products,
                                    start_parameter="one-month-subscription",
                                    payload="test-invoice-payload")
