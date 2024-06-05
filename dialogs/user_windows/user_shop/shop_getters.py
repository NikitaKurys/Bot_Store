from aiogram_dialog import DialogManager

from data_base.db_config import session
from data_base.requests.basket_requests import show_basket
from data_base.requests.category_requests import get_categories
from data_base.requests.product_requests import get_products


# Показать продукты
async def show_product(dialog_manager: DialogManager, **kwargs):
    checked_category = dialog_manager.dialog_data.get('is_checked')
    clicked_product = dialog_manager.dialog_data.get('clicked')
    user_id = kwargs['event_from_user'].id
    basket = await show_basket(session, user_id)
    current_page = await dialog_manager.find("stub_scroll").get_page()
    gender = dialog_manager.dialog_data.get('gender')
    products = []

    if dialog_manager.dialog_data.get("category").lower() == 'масло':  # Поскольку в БД категории "Масло" нет,
        dialog_manager.dialog_data.update(category="Духи")             # делаем замену
    category = dialog_manager.dialog_data.get("category")

    if category.lower() == 'духи':
        for product in await get_products(session, category, gender):
            products.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "category": product.category_id,
                    "gender": product.gender,
                    "price": product.price,
                    "img": product.path_to_img,
                    'Духи': [
                        ('5мл', product.price),
                        ('10мл', int(product.price * 2)),
                        ('15мл', int(product.price * 3)),
                        ('20мл', int(product.price * 3.8)),
                        ('30мл', int(product.price * 5.4)),
                        ('50мл', int(product.price * 8)),
                    ],
                    'Масло': [
                        ('3мл', int(product.price * 1.2)),
                        ('5мл', int(product.price * 2)),
                        ('8мл', int(product.price * 3.2)),
                        ('10мл', int(product.price * 4)),
                    ]
                }
            )

    else:
        for product in await get_products(session, category):
            products.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "category": product.category_id,
                    "gender": product.gender,
                    "price": int(product.price),
                    "img": product.path_to_img
                }
            )
    dialog_manager.dialog_data.update(product_id=products[current_page]['id'],
                                      product_price=products[current_page]['price'])

    if checked_category is None:
        checked_category = True
    if category == 'Духи' and checked_category is True:  # Изначально и при нажатии чекбоса
        add_oil = products[current_page]['Духи']                   # показываем цену духов
    elif category == 'Духи' and checked_category is False:
        add_oil = products[current_page]['Масло']
    else:
        add_oil = False
    return {
        "category": category,
        "checked": checked_category,
        "not_checked": not checked_category,
        "clicked": clicked_product,
        "pages": len(products),
        "products": products[current_page],
        'add_oil': add_oil,
        'not_oil': not add_oil,
        "basket": len(basket),
        "page": current_page + 1,
        }


# Показать категории
async def show_categories(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.dialog_data.get('is_checked')
    categories = []
    for category in await get_categories(session):
        categories.append((category.name, category.products))
    return {"categories": categories,
            "checked": checked,
            "not_checked": not checked}


# Показать категории
async def select_gender(**kwargs):
    gender = [
        (1, 'Мужские'),
        (2, 'Женские'),
        (3, 'Унисекс'),
        (4, 'Все'),
    ]
    return {
        'gender': gender
    }
