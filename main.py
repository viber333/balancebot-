import os
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

# ======= Настройки ==========
API_TOKEN = os.getenv("BOT_TOKEN", "7481381011:AAEosJJXY-Xn6UTRhVnCkZO9r5WXREyP-yw")
WEBHOOK_HOST = 'https://balancebot-j8tf.onrender.com'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

DATA_FILE = "data.json"

# ======= Работа с данными =======
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"balance": 0.0, "exchange_rate": 1.0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# ======= Команды ==========
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
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply("Пример: /setrate 75.5")
            return
        rate = float(parts[1])
        if rate <= 0:
            await message.reply("Курс должен быть больше нуля.")
            return
        data["exchange_rate"] = rate
        save_data(data)
        await message.reply(f"Курс установлен: {rate}")
    except ValueError:
        await message.reply("Ошибка: введи число, например /setrate 75.5")

@dp.message_handler(commands=['balance'])
async def cmd_balance(message: types.Message):
    await message.reply(f"Текущий баланс: {data['balance']:.2f}")

@dp.message_handler(commands=['resetbalance'])
async def cmd_resetbalance(message: types.Message):
    data["balance"] = 0.0
    save_data(data)
    await message.reply("Баланс сброшен.")

@dp.message_handler(commands=['resetrate'])
async def cmd_resetrate(message: types.Message):
    data["exchange_rate"] = 1.0
    save_data(data)
    await message.reply("Курс сброшен на 1.")

@dp.message_handler()
async def handle_number(message: types.Message):
    try:
        num = float(message.text.replace(',', '.'))
        rate = data["exchange_rate"]
        if rate == 0:
            await message.reply("Курс равен нулю, деление невозможно.")
            return
        added = num / rate
        data["balance"] += added
        save_data(data)
        await message.reply(f"Добавлено {added:.2f}. Новый баланс: {data['balance']:.2f}")
    except ValueError:
        await message.reply("Отправь число или команду.")

# ======= Webhook ==========
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook установлен")

async def on_shutdown(dp):
    logging.warning("Бот выключается...")
    await bot.delete_webhook()

# ======= Запуск ==========
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get('PORT', 10000))
    )
