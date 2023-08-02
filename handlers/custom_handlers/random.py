from aiogram import types
from config_data.config import API_KEY
from loader import dp
import requests

@dp.message_handler(commands=['random'])
async def random_movie_command(message: types.Message):
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
		rating = data['rating']['kp']
		genres = [genre['name'] for genre in data['genres']]
		countries = [country['name'] for country in data['countries']]
		description = data['description']
		link = f'https://www.kinopoisk.ru/film/{data["id"]}'
		movie_descr =(
			f'{name}{original_name} ({year})\n'
			f'Рейтинг Кинопоиск: {rating} / 10\n'
			f'Жанры: {", ".join(genres)}\n'
			f'Страны: {", ".join(countries)}\n'
			f'\n{description[:350]+"..."}\n'
			f'\n{link}')
		await message.answer_photo(poster, caption=movie_descr)
	except:
		await message.reply('Something went wrong. Try again in a while.')