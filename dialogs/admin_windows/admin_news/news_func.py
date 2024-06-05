from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram_dialog.widgets.kbd import Button

from data_base.db_config import session
from data_base.requests.user_requests import get_all_users


# Добавить контент
async def create_content(message: Message,
                         widget: MessageInput,
                         dialog_manager: DialogManager,
                         ):
    content = message.photo[-1].file_id
    dialog_manager.dialog_data.update(content=f"{content}")
    await dialog_manager.next()


# Добавить описание
async def create_caption(message: Message,
                         widget: MessageInput,
                         dialog_manager: DialogManager,
                         ):
    caption = message.text
    dialog_manager.dialog_data.update(caption=f"{caption}")
    await dialog_manager.next()


# Добавить ссылку
async def create_url(message: Message,
                     widget: MessageInput,
                     dialog_manager: DialogManager,
                     ):
    await message.answer('⬇️ Будет разослано следующее сообщение ⬇️')
    url = message.text
    dialog_manager.dialog_data.update(url=f"{url}")
    inline_button = InlineKeyboardButton(text=dialog_manager.dialog_data.get('url'),
                                         callback_data='check_news')
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[inline_button]]
    )
    await message.from_user.bot.send_photo(chat_id=message.chat.id,
                                           photo=dialog_manager.dialog_data['content'],
                                           caption=dialog_manager.dialog_data['caption'],
                                           reply_markup=inline_kb)
    await dialog_manager.next()


# Разослать сообщения
async def spam_news(clb: CallbackQuery,
                    widget: Button,
                    dialog_manager: DialogManager,
                    ):
    inline_button = InlineKeyboardButton(text=dialog_manager.dialog_data.get('url'),
                                         callback_data='check_news')
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[[inline_button]]
    )
    for user in await get_all_users(async_session=session):
        await clb.from_user.bot.send_photo(chat_id=user.id,
                                           photo=dialog_manager.dialog_data['content'],
                                           caption=dialog_manager.dialog_data['caption'],
                                           reply_markup=inline_kb)
    await clb.answer('Рассылка завершена!')
    await dialog_manager.done()
