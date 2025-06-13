import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN", "7481381011:AAEosJJXY-Xn6UTRhVnCkZO9r5WXREyP-yw")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"balance": 0.0, "rate": 1.0}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Отправь число, и я поделю его на курс и прибавлю к балансу.\n"
        "/setrate <число> — задать курс\n"
        "/balance — показать баланс\n"
        "/resetbalance — сбросить баланс\n"
        "/resetrate — сбросить курс"
    )

@dp.message_handler(commands=['setrate'])
async def setrate(message: types.Message):
    data = load_data()
    try:
        parts = message.text.split()
        rate = float(parts[1])
        if rate <= 0:
            await message.answer("Курс должен быть больше нуля.")
            return
        data['rate'] = rate
        save_data(data)
        await message.answer(f"Курс установлен: {rate}")
    except:
        await message.answer("Пример: /setrate 75.5")

@dp.message_handler(commands=['balance'])
async def balance_cmd(message: types.Message):
    data = load_data()
    await message.answer(f"Баланс: {data['balance']:.2f}")

@dp.message_handler(commands=['resetbalance'])
async def reset_balance(message: types.Message):
    data = load_data()
    data['balance'] = 0.0
    save_data(data)
    await message.answer("Баланс сброшен.")

@dp.message_handler(commands=['resetrate'])
async def reset_rate(message: types.Message):
    data = load_data()
    data['rate'] = 1.0
    save_data(data)
    await message.answer("Курс сброшен на 1.")

@dp.message_handler()
async def add_amount(message: types.Message):
    data = load_data()
    try:
        value = float(message.text.replace(',', '.'))
        added = value / data['rate']
        data['balance'] += added
        save_data(data)
        await message.answer(f"Добавлено: {added:.2f}. Баланс: {data['balance']:.2f}")
    except:
        await message.answer("Отправь число или используй команды.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
