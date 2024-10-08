from urllib.parse import urlparse, parse_qs
from typing import List
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кроссовки")],
        [KeyboardButton(text="Обновить данные")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню",
)


async def create_product_keyboard(
    products: List[dict], page: int, total_pages: int
) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()

    for product_key in products:
        product_values = products[product_key]
        product_title = product_values["product"]["title"]

        parsed_url = urlparse(product_key)
        query_params = parse_qs(parsed_url.query)
        sku_id = query_params.get("skuId", [None])[0]

        button = InlineKeyboardButton(text=product_title, callback_data=sku_id)
        keyboard_builder.add(button)

    if page > 0:
        keyboard_builder.add(
            InlineKeyboardButton(text="Назад", callback_data=f"products:{page - 1}")
        )
    if page < total_pages - 1:
        keyboard_builder.add(
            InlineKeyboardButton(text="Далее", callback_data=f"products:{page + 1}")
        )

    return keyboard_builder.adjust(3).as_markup()


cancel = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="cancel")]]
)
