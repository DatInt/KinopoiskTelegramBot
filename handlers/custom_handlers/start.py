from aiogram import types

from loader import dp


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
		await message.reply('Привет! Открой меню и выбери комманду.')
