from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Group, Row, Start, Button, Column, Cancel, Back

from dialogs.admin_windows.admin_news.news_func import create_content, create_caption, create_url, spam_news
from dialogs.admin_windows.admin_states import CategoryStates, NewsStates, AdminStates
from dialogs.user_windows.user_main.user_getters import get_username

content_window = Window(
    Const('Скиньте фото новости'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=create_content,
        content_types=ContentType.ANY,
    ),
    Column(
        Cancel(Const("◀️ Вернуться"), id="cancel"),
    ),
    state=NewsStates.content_state,
    getter=get_username,
)

caption_window = Window(
    Const('Напиши описание к фото'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=create_caption,
        content_types=ContentType.TEXT,
    ),
    Column(
        Cancel(Const("◀️ Вернуться"), id="cancel"),
    ),
    state=NewsStates.caption_state,
    getter=get_username,
)


url_window = Window(
    Const('Напиши название ссылки'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=create_url,
        content_types=ContentType.TEXT,
    ),
    Column(
        Cancel(Const("◀️ Вернуться"), id="cancel"),
    ),
    state=NewsStates.url_name_state,
    getter=get_username,
)


success_window = Window(
    Const('Рассылаем?'),
    Group(
      Row(
          Button(text=Const('ДА 👍'), id='yes', on_click=spam_news),
          Start(text=Const('НЕТ ❌'), id='no', state=AdminStates.admin_state),
      ),
    ),
    state=NewsStates.success_state,
    getter=get_username,
)
