from aiogram.fsm.state import StatesGroup, State


class SearchState(StatesGroup):
    query = State()


class FilmCreateState(StatesGroup):
    name = State()
    year = State()
    rating = State()
    genre = State()
    actors = State()
    description = State()
    poster = State()


class MovieDeleteState(StatesGroup):
    query = State()
