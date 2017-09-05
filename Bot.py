import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
import json
import time

# Telegram bot setup
updater = Updater(token="406484014:AAH0ik5seLM0bI07aUY78kMMiZaPuCtLAyA")
bot = telegram.Bot(token="406484014:AAH0ik5seLM0bI07aUY78kMMiZaPuCtLAyA")
dispatcher = updater.dispatcher

# GET request from football-data.org
url = "http://api.football-data.org/v1/fixtures/"
querystring = {"league":"PL","timeFrame":"n7"}
headers = {
    'x-auth-token': "0c0d4ed2886a44bfa2434fe958103dac",
    'x-response-control': "minified",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
response_json = json.loads(response.text)

## Fixture list from GET request

def result(input):

    str_print = "== Upcoming Fixtures ==\n\n"

    for i in response_json["fixtures"]:
        str_print += i["homeTeamName"] + " v " + i["awayTeamName"] + "\nDate: " + i["date"][:10] + "\nKickoff: " + i["date"][11:16] + "\n\n"

    return str_print

## Bot command functions

def start(bot, update):

    bot.send_message(chat_id=update.message.chat_id, text="Bot started!")

def fixture(bot, update):

    bot.send_message(chat_id=update.message.chat_id, text=result(response_json))

## Main section - bot commands

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

fixture_handler = CommandHandler('fixture', fixture)
dispatcher.add_handler(fixture_handler)

updater.start_polling()

## Make sure bot is running

print()
print("Running...")
print()
print()

## Keep bot active on Heroku - print something every 5 mins

# starttime = time.time()
#
# while True:
#     print("tick")
#     time.sleep(600.0 - ((time.time() - starttime) % 600.0))