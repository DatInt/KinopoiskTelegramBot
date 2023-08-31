from aiogram import types
from config_data.config import API_KEY
from loader import dp
import requests
from keyboards.inline.random_button import keyboard
from loader import dp, bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.database import User


@dp.message_handler(commands=['random'])
async def random_movie_command(message: types.Message, *args):
	"""
	Хендлер для поиска случайного фильма в базе кинопоиска
	"""
	try:
		request = requests.get(f'https://api.kinopoisk.dev/v1.3/movie/random', headers={'X-API-KEY': API_KEY})
		data = request.json()
		poster = data['poster']['url']
		name = data['name']
		original_name = data['alternativeName']
		if original_name is None:
			original_name = ''
		else:
			original_name = ' / ' + str(data['alternativeName'])
		year = data['year']
		rating = round(data['rating']['kp'], 1)
		genres = [genre['name'] for genre in data['genres']]
		countries = [country['name'] for country in data['countries']]
		description = data['description']
		link = f'https://www.kinopoisk.ru/film/{data["id"]}'
		movie_descr = (
			f'{name}{original_name} ({year})\n'
			f'Рейтинг Кинопоиск: {rating}/10⭐️\n'
			f'Жанры: {", ".join(genres)}\n'
			f'Страны: {", ".join(countries)}\n'
			f'\n{description[:350] + "..."}\n'
			f'\n{link}')
		try:
			if callback_user_id:
				user_id = callback_user_id
			else:
				user_id = message.from_user.id
			if callback_username:
				username = callback_username
			else:
				username = message.from_user.username
			User.create(user_id=user_id, username=username, link=link, movie_name=name, year=year)
		except Exception as Ex:
			print(Ex)
		await message.answer_photo(poster, caption=movie_descr, reply_markup=keyboard)
	except:
		await message.answer('Что-то пошло не так, попробуйте снова позже')


@dp.callback_query_handler(lambda c: c.data == 'refresh')
async def process_callback_button(callback_query: types.CallbackQuery):
	"""
	Хендлер для обработки нажатия кнопки поиска другого фильма.
	"""
	print(callback_query.from_user.username)
	callback_user_id = callback_query.from_user.id
	callback_username = callback_query.from_user.username
	await random_movie_command(callback_query.message, callback_user_id, callback_username)


