from aiogram_dialog import Dialog
from dialogs.user_windows.user_main import user_windows
from dialogs.user_windows.user_shop import shop_windows
from dialogs.user_windows.user_basket import basket_windows
from dialogs.user_windows.user_pay import pay_windows

user_dialog = Dialog(
    user_windows.menu_window,
    user_windows.contacts_window,
    user_windows.about_us_window,
)

shop_dialog = Dialog(
    shop_windows.category_window,
    shop_windows.product_window,
    shop_windows.gender_window
)

basket_dialog = Dialog(
    basket_windows.basket_window,
)

pay_dialog = Dialog(
    pay_windows.select_location_window,
    pay_windows.location_window,
    pay_windows.contact_window,
    pay_windows.check_window
)
