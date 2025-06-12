from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN", "7481381011:AAEosJJXY-Xn6UTRhVnCkZO9r5WXREyP-yw")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Начальный баланс и курс
balance = 0.0
exchange_rate = 1.0  # по умолчанию

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Отправь число, и я поделю его на курс и добавлю к балансу.\n"
        "Команда /setrate <число> — чтобы задать курс.\n"
        "Команда /balance — посмотреть баланс.\n"
        "Команда /resetbalance — сбросить баланс в 0.\n"
        "Команда /resetrate — сбросить курс на 1."
    )

@dp.message_handler(commands=['setrate'])
async def cmd_setrate(message: types.Message):
    global exchange_rate
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply("Пожалуйста, введи курс после команды, например:\n/setrate 75.5")
            return
        rate = float(parts[1])
        if rate <= 0:
            await message.reply("Курс должен быть положительным числом.")
            return
        exchange_rate = rate
        await message.reply(f"Курс установлен на {exchange_rate}")
    except ValueError:
        await message.reply("Неправильный формат курса. Используй число, например:\n/setrate 75.5")

@dp.message_handler(commands=['balance'])
async def cmd_balance(message: types.Message):
    await message.reply(f"Текущий баланс: {balance:.2f}")

@dp.message_handler(commands=['resetbalance'])
async def cmd_resetbalance(message: types.Message):
    global balance
    balance = 0.0
    await message.reply("Баланс сброшен в 0.")

@dp.message_handler(commands=['resetrate'])
async def cmd_resetrate(message: types.Message):
    global exchange_rate
    exchange_rate = 1.0
    await message.reply("Курс сброшен на 1.")

@dp.message_handler()
async def handle_number(message: types.Message):
    global balance, exchange_rate
    try:
        num = float(message.text.replace(',', '.'))
        if exchange_rate == 0:
            await message.reply("Курс равен нулю, деление невозможно.")
            return
        added = num / exchange_rate
        balance += added
        await message.reply(f"Добавлено {added:.2f} к балансу.\nНовый баланс: {balance:.2f}")
    except ValueError:
        await message.reply("Пожалуйста, отправь число или команду.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
