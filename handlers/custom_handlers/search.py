from aiogram import types
from config_data.config import API_KEY
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from states.states import Search
import requests
from keyboards.inline.search_again import keyboard
from database.database import User, Movies


@dp.message_handler(commands=['search'], state=None)
async def search_movie_command(message: types.Message):
	"""
	Хендлер реагирующий на команду /search и получающий название фильма от пользователя
	"""
	await bot.send_message(message.from_user.id, text="Введите название фильма для поиска: ")
	await Search.search_name.set()


@dp.message_handler(state=Search.search_name)
async def search_movies_list_by_name(message: types.Message, state: FSMContext):
	"""
	Хендлер для поиска фильма по названию в базе кинопоиска
	"""
	try:
		movie_name = message.text
		request = requests.get(f'https://api.kinopoisk.dev/v1.3/movie?name={movie_name}', headers={'X-API-KEY': API_KEY})
		data = request.json()
		movies_list = data['docs']
		await message.answer(f'Найдено результатов: {len(movies_list)}')
		if movies_list:
			for movie in movies_list:
				genres = []
				countries = []
				description = ''
				poster = open('utils/misc/blank.jpg', 'rb')
				if movie['poster']:
					poster = movie['poster']['url']
				name = movie['name']
				original_name = movie['alternativeName']
				if original_name is None:
					original_name = ''
				else:
					original_name = ' / ' + str(movie['alternativeName'])
				year = movie['year']
				rating = round(movie['rating']['kp'], 1)
				if movie['genres']:
					genres = [genre['name'] for genre in movie['genres']]
				if movie['countries']:
					countries = [country['name'] for country in movie['countries']]
				if movie['description']:
					description = movie['description']
				link = f'https://www.kinopoisk.ru/film/{movie["id"]}'
				movie_descr = (
					f'{name}{original_name} ({year})\n'
					f'Рейтинг: {rating}/10⭐️\n'
					f'Жанры: {", ".join(genres)}\n'
					f'Страны: {", ".join(countries)}\n'
					f'\n{description[:350] + "..."}\n'
					f'\n{link}')
				try:
					user_id = message.from_user.id
					username = message.from_user.username
					try:
						user = User.create(user_id=user_id, username=username)
						Movies.create(user=user, link=link, movie_name=name, year=year, category='search')
					except:
						user = User.get(User.user_id == user_id)
						Movies.create(user=user, link=link, movie_name=name, year=year, category='search')
				except Exception as Ex:
					print(Ex)
				await message.answer_photo(poster, caption=movie_descr)
				await state.finish()
		else:
			await message.answer(f'Фильм {movie_name} не найден.')
			await state.finish()
		await message.answer(text='Не нашли что искали? Повторите поиск', reply_markup=keyboard)
	except:
		await message.answer('Что-то пошло не так, попробуйте позже')


@dp.callback_query_handler(lambda c: c.data == 're_search', state=None)
async def process_callback_button(message: types.Message):
	"""
	Хендлер для обработки кнопки повторного поиска
	"""
	await bot.send_message(message.from_user.id, text="Введите название фильма для поиска: ")
	await Search.search_name.set()
