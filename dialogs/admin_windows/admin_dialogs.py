from aiogram_dialog import Dialog

from dialogs.admin_windows.admin_main import admin_windows
from dialogs.admin_windows.admin_logs import logs_windows
from dialogs.admin_windows.admin_products import product_windows
from dialogs.admin_windows.admin_news import news_windows
from dialogs.admin_windows.admin_category import category_windows
from dialogs.admin_windows.add_admin import add_admins_windows

admin_dialog = Dialog(
    admin_windows.menu_window,
)

logs_dialog = Dialog(
    logs_windows.logs_window,
    logs_windows.buy_logs_window,
    logs_windows.subscribers_logs_window
)

add_admin_dialog = Dialog(
    add_admins_windows.show_admin_window,
    add_admins_windows.create_admin_window,
)

news_dialog = Dialog(
    news_windows.content_window,
    news_windows.caption_window,
    news_windows.url_window,
    news_windows.success_window
)

category_dialog = Dialog(
    category_windows.category_window,
    category_windows.add_category_window,
    category_windows.del_category_window,
    category_windows.update_category_window,
    category_windows.rename_category_window,
)

product_dialog = Dialog(
    product_windows.product_window,
    product_windows.add_product_window,
    product_windows.add_product_photo,
    product_windows.add_product_description,
    product_windows.add_product_price,
    product_windows.add_product_gender,

    product_windows.update_product_window,
    product_windows.update_name_window,
    product_windows.update_description_window,
    product_windows.update_product_gender,
    product_windows.update_price_window,
    product_windows.update_product_photo,
    product_windows.update_product_category
)
