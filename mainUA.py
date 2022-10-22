import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup
import logging


open_weather_token = "токен openWeather"
tg_bot_token = "токен бота"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⛅️Погода⛅️"))
    markup.add(types.KeyboardButton("💰Курс валют💰"))
    await message.answer("Обери одну з функцій внизу", reply_markup=markup)



#💰💷💶💴💵
@dp.message_handler(lambda message: message.text == "💰Курс валют💰")
async def exchange_rates(message: types.Message):
    url="https://minfin.com.ua/ua/currency/"
    rs=requests.get(url)
    soup = BeautifulSoup(rs.text, 'lxml')
    nby = soup.find_all('span', class_='mfcur-nbu-full-wrap')
    buy = soup.find_all('td', class_='mfm-text-nowrap')
    sell = soup.find_all('td', class_='mfm-text-nowrap')
    await message.reply(f"\U0001F4B5 USD:\n НБУ: {nby[0].text[1:8]} Купівля: {buy[1].text[1:8]} Продаж:{sell[1].text[14:20]}\n\n"
                        f"\U0001F4B6 EUR:\n НБУ: {nby[1].text[1:8]} Купівля: {buy[3].text[1:8]} Продаж:{sell[3].text[14:20]}\n\n")



@dp.message_handler(lambda message: message.text == "⛅️Погода⛅️")
async def name_city(message: types.Message):
    await message.reply("Введіть назву міста: ")

    @dp.message_handler(lambda message: message.text != "💰Курс валют💰")
    async def get_weather(message: types.Message):
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Хмарно \U00002601",
            "Rain": "Дощ  \U00002614",
            "Drizzle": "Дощ  \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Сніг \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
            )
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "🤷 Я не розумію, яка там погода 🤷"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                f"Погода в місті: {city}\nТемпература: {cur_weather}C° {wd}\n"
                f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nВітер: {wind} м/с\n"
                f"Схід сонця: {sunrise_timestamp}\nзахід сонця: {sunset_timestamp}\nТривалість дня: {length_of_the_day}\n"
                f"***Гарного дня!*** "
                )

        except:
            await message.reply("🔎Місто не знайдено🔎")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
