from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    menu_state = State()
    contacts_state = State()
    about_us_state = State()


class ShopStates(StatesGroup):
    category_states = State()
    product_states = State()
    gender_states = State()


class BasketStates(StatesGroup):
    menu_state = State()
    delete_state = State()


class PayStates(StatesGroup):
    select_location_state = State()
    location_state = State()
    contact_state = State()
    check_state = State()
    pay_state = State()
