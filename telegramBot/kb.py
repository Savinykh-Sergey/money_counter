from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


menu = ReplyKeyboardBuilder()
menu.row(
    KeyboardButton(text="Загрузить фото", callback_data="load_photo"),
    KeyboardButton(text="Избранное", callback_data="favorite"),
    KeyboardButton(text="История", callback_data="history")
)
menu.row(
    KeyboardButton(text="Баланс", callback_data="balance")
)


menu_admin = ReplyKeyboardBuilder()
menu_admin.row(
    KeyboardButton(text="Статистика пользователей", callback_data="user_statistics"),
    KeyboardButton(text="Запросы пользователей", callback_data="user_statistics"),
    KeyboardButton(text="Статистика пользователей", callback_data="user_statistics"),
    KeyboardButton(text="Выдать привилегию", callback_data="grant_privilege")
)


evaluation_neural_network = [
    [InlineKeyboardButton(text="👍", callback_data="right"),
    InlineKeyboardButton(text="👎", callback_data="wrong")],
    [InlineKeyboardButton(text="Добавить в избранное", callback_data="add_favorite")]
]
evaluation_neural_network = InlineKeyboardMarkup(inline_keyboard=evaluation_neural_network)


del_favorite_photo = [
    [InlineKeyboardButton(text="Удалить из избранного", callback_data="del_photo")]
]
del_favorite_photo = InlineKeyboardMarkup(inline_keyboard=del_favorite_photo)