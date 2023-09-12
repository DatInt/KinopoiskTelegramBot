from loader import dp, bot
import handlers
import logging
from aiogram.utils import executor
from database.controllers import create_tables

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

if __name__ == "__main__":
    create_tables()
    executor.start_polling(dp)
