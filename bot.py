import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog import setup_dialogs, DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from config.config_data import load_config, Config
from data_base.db_config import engine
from data_base.models import Base
from dialogs.admin_windows import admin_dialogs
from dialogs.user_windows import user_dialogs
from dialogs.user_windows.user_main import user_windows
from handlers import user_handlers, admin_handlers

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def on_unknown_intent(event, dialog_manager: DialogManager):
    # Example of handling UnknownIntent Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        user_windows.menu_window, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND,
    )


async def on_unknown_state(event, dialog_manager: DialogManager):
    # Example of handling UnknownState Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        user_windows.menu_window, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND,
    )


async def main():
    config: Config = load_config()

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher()

    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        on_unknown_state,
        ExceptionTypeFilter(UnknownState),
    )

    dp.include_routers(user_handlers.router, user_dialogs.user_dialog,
                       user_dialogs.pay_dialog, user_dialogs.shop_dialog,
                       user_dialogs.basket_dialog,
                       admin_handlers.router,
                       admin_dialogs.admin_dialog, admin_dialogs.category_dialog,
                       admin_dialogs.news_dialog, admin_dialogs.product_dialog,
                       admin_dialogs.logs_dialog, admin_dialogs.add_admin_dialog
                       )
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
