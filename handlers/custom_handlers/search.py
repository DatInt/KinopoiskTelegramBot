from aiogram import types
from config_data.config import API_KEY
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from states.states import Search
import requests

@dp.message_handler(commands=['search'], state=None)
async def search_movie_command(message: types.Message):
	await bot.send_message(message.from_user.id, text="Введите название фильма для поиска: ")
	await Search.search_name.set()

@dp.message_handler(state=Search.search_name)
async def search_movie_by_name(message: types.Message, state: FSMContext):
	try:
		movie_name = message.text
		request = requests.get(f'https://api.kinopoisk.dev/v1.3/movie?name={movie_name}&limit=1',
													 headers={'X-API-KEY': API_KEY})
		data = request.json()
		print(data)
		poster = data['docs'][0]['poster']['url']
		name = data['docs'][0]['name']
		original_name = data['docs'][0]['alternativeName']
		if original_name is None:
			original_name = ''
		else:
			original_name = ' / ' + str(data['docs'][0]['alternativeName'])
		year = data['docs'][0]['year']
		rating = data['docs'][0]['rating']['kp']
		genres = [genre['name'] for genre in data['docs'][0]['genres']]
		countries = [country['name'] for country in data['docs'][0]['countries']]
		description = data['docs'][0]['description']
		link = f'https://www.kinopoisk.ru/film/{data["docs"][0]["id"]}'
		movie_descr = (
			f'{name}{original_name} ({year})\n'
			f'Рейтинг Кинопоиск: {rating} / 10\n'
			f'Жанры: {", ".join(genres)}\n'
			f'Страны: {", ".join(countries)}\n'
			f'\n{description[:350] + "..."}\n'
			f'\n{link}')
		await message.answer_photo(poster, caption=movie_descr)
		await state.finish()
	except:
		await message.reply('Film was not found. Try again.')