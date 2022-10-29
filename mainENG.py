import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup
import logging


open_weather_token = "your opernWeather token"
tg_bot_token = "your bot token"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⛅️Weather⛅️"))
    markup.add(types.KeyboardButton("💰Exchange rate💰"))
    await message.answer("Select one of the functions below", reply_markup=markup)


#💰💷💶💴💵
@dp.message_handler(lambda message: message.text == "💰Exchange rate💰")
async def exchange_rates(message: types.Message):
    url="https://minfin.com.ua/ua/currency/"
    rs=requests.get(url)
    soup = BeautifulSoup(rs.text, 'lxml')
    nby = soup.find_all('span', class_='mfcur-nbu-full-wrap')
    buy = soup.find_all('td', class_='mfm-text-nowrap')
    sell = soup.find_all('td', class_='mfm-text-nowrap')
    await message.reply(f"\U0001F4B5 USD:\n NBU: {nby[0].text[1:8]} Buy: {buy[1].text[1:8]} Sell:{sell[1].text[14:20]}\n\n"
                        f"\U0001F4B6 EUR:\n NBU: {nby[1].text[1:8]} Buy: {buy[3].text[1:8]} Sell:{sell[3].text[14:20]}\n\n")



@dp.message_handler(lambda message: message.text == "⛅️Weather⛅️")
async def name_city(message: types.Message):
    await message.reply("Enter the name of the city: ")

    @dp.message_handler(lambda message: message.text != "💰Exchange rate💰")
    async def get_weather(message: types.Message):
        code_to_smile = {
            "Clear": "Clear \U00002600",
            "Clouds": "Clouds \U00002601",
            "Rain": "Rain \U00002614",
            "Drizzle": "Drizzle \U00002614",
            "Thunderstorm": "Thunderstorm \U000026A1",
            "Snow": "Snow \U0001F328",
            "Mist": "Mist \U0001F32B"
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
                wd = "🤷 I don't know what the weather is like 🤷"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                f"Weather in the city: {city}\nTemperature: {cur_weather}C° {wd}\n"
                f"Humidity: {humidity}%\nPressure: {pressure} mmHg\nWind: {wind} m/s\n"
                f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nLength of day: {length_of_the_day}\n"
                f"***Have a nice day!***"
                ) 

        except:
            await message.reply("🔎City not found🔎")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
