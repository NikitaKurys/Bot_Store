from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    admin_state = State()


class AddAdminStates(StatesGroup):
    show_admin_state = State()
    add_admin_state = State()
    del_admin_state = State()


class AdminLogsStates(StatesGroup):
    logs_state = State()
    buy_state = State()
    subscribers_state = State()


class NewsStates(StatesGroup):
    content_state = State()
    caption_state = State()
    url_name_state = State()
    success_state = State()
    

class CategoryStates(StatesGroup):
    category_state = State()
    add_category_state = State()
    del_category_state = State()
    update_category_state = State()
    rename_category_state = State()


class ProductStates(StatesGroup):
    product_state = State()

    add_name_state = State()
    add_photo_state = State()
    add_description_state = State()
    add_price_state = State()
    add_gender_state = State()

    del_product_state = State()

    update_product_state = State()
    update_name_state = State()
    update_description_state = State()
    update_price_state = State()
    update_gender_state = State()
    update_category_state = State()
    update_photo_state = State()
