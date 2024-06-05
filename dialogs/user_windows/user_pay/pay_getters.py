from aiogram_dialog import DialogManager

from data_base.models import User


# Проверка данных
async def get_check(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    location = dialog_manager.dialog_data.get("location")
    contact = dialog_manager.dialog_data.get("contact")
    summ_price = 0
    for price in dialog_manager.start_data[0]:
        summ_price += int(price['price'])
    dialog_manager.dialog_data.update(summ_price=summ_price)
    return {
        "location": location,
        "contact": contact,
        "username": event_from_user.first_name,
        "summ_price": summ_price,
    }


# Выбор доставки
async def get_delivery(dialog_manager: DialogManager, **kwargs):
    delivery = [
        (1, 'Почта России 📪'),
        (2, 'СДЭК 📩'),
    ]
    mail = False
    sdek = False
    location = dialog_manager.dialog_data.get('location')
    if location == 'Почта России 📪':
        mail = True
    else:
        sdek = True
    return {
        "delivery": delivery,
        "mail": mail,
        "sdek": sdek,
    }
