from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class FilmCallback(CallbackData, prefix="film", sep=";"):
    id: int
    name: str


def films_keyboard_markup(films_list):
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)

    for index, film in enumerate(films_list):
        callback_data = FilmCallback(id=index, name=film["name"])
        builder.button(
            text=film["name"], callback_data=FilmCallback(id=index, name=film["name"])
        )

    return builder.as_markup()
