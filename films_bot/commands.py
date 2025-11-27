from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START_COMMAND = Command("start")
FILMS_COMMAND = Command("films")
FILM_CREATE_COMMAND = Command("create_film")
FILM_SEARCH_COMMAND = Command("search_film")

START_BOT_COMMAND = BotCommand(command="start", description="Почати розмову")
FILMS_BOT_COMMAND = BotCommand(command="films", description="Перегляд списку фільмів")
FILM_CREATE_BOT_COMMAND = BotCommand(command="create_film", description="Додати фільм")
FILM_SEARCH_BOT_COMMAND = BotCommand(command="search_film", description="Знайти фільм за назвою")
FILM_DELETED_BOT_COMMAND = BotCommand(command="delete_film", description="Видалити фільм за назвю")