from random import randint
from TOKEN import TOKEN
import json
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import Message
city_name = " "
bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет! ")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	if message.text == "/weather":
		bot.send_message(message.from_user.id,'Напиши свой город ')
		bot.register_next_step_handler(message,Weather_bot)
	else:
		bot.reply_to(message, "Невереная команда")
        
def roll(message):
    bot.send_message(message.from_user.id,randint(0,100))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	if message.text == "/roll":

		bot.send_message(message,roll)
	else:
		bot.reply_to(message, roll)   



def Weather_bot(message):
    global city_name 
    city_name = message.text
    Url_for_current_weather = 'http://api.openweathermap.org/data/2.5/weather?'
    params={
    'q':city_name,
    'appid':'c73eeb1e755f23ecb9fe710f40ee296a',
    'units':'metric',
    'lang':'ru'
    }#погода на данный момент
    Response = requests.get(Url_for_current_weather, params=params)
    item = Response.json()
    try:
        lon=item['coord']['lon']
        lat=item['coord']['lat']
    except:
        bot.send_message(message.from_user.id,("Нет такого города"))
    Url_for_onecall='https://api.openweathermap.org/data/2.5/onecall?'
    params={
    'lat':lat,
    'lon':lon,
    'exclude':'current,minutely,hourly',
    'appid':'c73eeb1e755f23ecb9fe710f40ee296a',
    'units':'metric',
    'lang':'ru'
    }
    Response = requests.get(Url_for_onecall, params=params)
    item = Response.json()
    weather=item['daily'][0]['weather']
    temp=item['daily'][0]['temp']
    try:
        bot.send_message(message.from_user.id,"Погода :" + ' ' + weather[0]['description'] + '\n'  
       +'Дневная температура :'+' ' + str(int(temp['day'])) + '°C' + '\n'
        +'Температура ночью  :'+' ' + str(int(temp['night'])) + '°C' + '\n' 
        +'Скорость ветра :' + ' ' + str(int(item['daily'][0]['wind_speed'])) + 'м\с'+'\n'
        +'Давление :'+ ' ' + str(item['daily'][0]['pressure']) + 'мм рт. ст.')  
    except :
        bot.send_message(message.from_user.id,"Населенный пункт не найден")
bot.infinity_polling()

