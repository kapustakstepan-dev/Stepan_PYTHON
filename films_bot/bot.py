import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN
from data import get_films, add_film, search_films, save_films
from keyboards import films_keyboard_markup, FilmCallback
from states import SearchState, FilmCreateState, MovieDeleteState

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# start of telegram bot
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Я кіно-бот \n\n"
        "Команди:\n"
        "/films – список фільмів\n"
        "/create_film – додати новий фільм\n"
        "/search_film – пошук фільму\n"
        "/delete_film – видалити фільм"
    )


# show the fimls
@dp.message(Command("films"))
async def cmd_films(message: types.Message):
    films = get_films()
    markup = films_keyboard_markup(films)
    await message.answer("Список фільмів ", reply_markup=markup)


@dp.callback_query(FilmCallback.filter())
async def callback_film(callback: FilmCallback, callback_data: types.Message):
    film = get_films(film_id=callback_data.id)

    text = (
        f"<b>{film.get('name')}</b>\n"
        f"Рік: {film.get('year', 'не вказано')}\n"
        f"Рейтинг: {film.get('rating', 'не вказано')}\n"
        f"Жанр: {film.get('genre', 'не вказано')}\n"
        f"Актори: {', '.join(film.get('actors', []))}\n\n"
        f"{film.get('description')}"
    )

    await callback.message.answer_photo(
        film.get("poster"),
        caption=text,
    )
    await callback.answer()


# create the film#
@dp.message(Command("create_film"))
async def start_create(message: types.Message, state: FSMContext):
    await message.answer("Введіть назву фільму -> ")
    await state.set_state(FilmCreateState.name)


@dp.message(FilmCreateState.name)
async def film_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть рік впуску фільму -> ")
    await state.set_state(FilmCreateState.year)


@dp.message(FilmCreateState.year)
async def film_year(message: types.Message, state: FSMContext):
    await state.update_data(year=int(message.text))
    await message.answer("Опишіть фільм -> ")
    await state.set_state(FilmCreateState.description)


@dp.message(FilmCreateState.description)
async def film_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введіть рейтенгу фільма -> ")
    await state.set_state(FilmCreateState.rating)


@dp.message(FilmCreateState.rating)
async def film_rating(message: types.Message, state: FSMContext):
    await state.update_data(rating=float(message.text))
    await message.answer("Введіть жанр -> ")
    await state.set_state(FilmCreateState.genre)


@dp.message(FilmCreateState.genre)
async def film_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer("Введіть акторів через клму-> ")
    await state.set_state(FilmCreateState.actors)


@dp.message(FilmCreateState.actors)
async def film_actors(message: types.Message, state: FSMContext):
    actors_lst = [j.strip() for j in message.text.split(",")]
    await state.update_data(actors=actors_lst)
    await message.answer("Вставте URL постера -> ")
    await state.set_state(FilmCreateState.poster)


@dp.message(FilmCreateState.poster)
async def film_poster(message: types.Message, state: FSMContext):
    await state.update_data(poster=message.text)
    film = await state.get_data()

    add_film(film)
    await message.answer("Фільм додано в колекцію! ")
    await state.clear()


# search film in json
@dp.message(Command("search_film"))
async def start_search(message: types.Message, state: FSMContext):
    await message.answer("Введіть назву фільму -> ")
    await state.set_state(SearchState.query)


@dp.message(SearchState.query)
async def search_process(message: types.Message, state: FSMContext):
    query = message.text
    results = search_films(query)
    await state.clear()

    if not results:
        await message.answer("За цією назвою нічого не знайденно ")
        return

    text = "Знайдені фільми:\n\n"

    for film in results:
        text += f"{film["name"]} - {film.get("rating", "? ")}\n\n"

    await message.answer(text)


# delete films
@dp.message(Command("delete_film"))
async def start_delete(message: types.Message, state: FSMContext):
    await message.answer("Введіть назву фільму, який хочете видалити -> ")
    await state.set_state(MovieDeleteState.query)


@dp.message(MovieDeleteState.query)
async def delete_process(message: types.Message, state: FSMContext):
    name = message.text.lower()
    films = get_films()

    for film in films:
        if film["name"].lower() == name:
            films.remove(film)
            save_films(films)
            await message.answer(f" Видалено -> {film["name"]} ")
            await state.clear()
            return

    await message.answer("Фільм не знайдено ")
    await state.clear()


if __name__ == "__main__":

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
