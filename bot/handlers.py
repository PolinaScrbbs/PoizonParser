from aiogram import F, Bot, Router
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from parser.main import start_parser

from .config import PRODUCTS_PER_PAGE
from . import keyboards as kb
from .utils import load_product_data
from .response import get_yuan_rate

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.username}, выберите пункит из меню",
        reply_markup=kb.start,
    )


@router.message(lambda message: message.text == "Кроссовки")
async def send_product_info(message: Message, page: int = 0):
    product_data = await load_product_data()
    product_keys = list(product_data.keys())
    total_pages = (len(product_data) + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE

    start_index = page * PRODUCTS_PER_PAGE
    end_index = start_index + PRODUCTS_PER_PAGE
    current_product_keys = product_keys[start_index:end_index]
    current_products = {key: product_data[key] for key in current_product_keys}

    keyboard = await kb.create_product_keyboard(current_products, page, total_pages)
    await message.answer("Выберите фото или размер кроссовок:", reply_markup=keyboard)


@router.callback_query(lambda callback: callback.data.startswith("products:"))
async def paginate_products(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await send_product_info(callback.message, page)


@router.callback_query(lambda callback: callback.data.isdigit())
async def product_callback_handler(callback: CallbackQuery):
    sku_id = callback.data
    product_data = await load_product_data()

    product_key = next((key for key in product_data if f"skuId={sku_id}" in key), None)
    yuan_rate = await get_yuan_rate()

    if product_key:
        product_info = product_data[product_key]
        product = product_info["product"]
        title = product["title"]
        price = round(int(product["price"]) * yuan_rate, 2)
        size_list = ", ".join(product["size_list"])

        button_link = InlineKeyboardButton(text="Перейти", url=product_key)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_link]])

        await callback.message.answer(
            f"Название: {title}\nЦена: {price}₽\nДоступные размеры: {size_list}",
            reply_markup=keyboard,
        )
    else:
        await callback.message.answer("Товар не найден.")


@router.message(lambda message: message.text == "Обновить данные")
async def update_data(message: Message):
    await message.answer("Данные обновляются, пожалуйста подождите")
    status, error = start_parser()
    if status:
        await message.answer("Обновление данных завершено")
    else:
        await message.answer(f"Произошла ошибка: {error}")
