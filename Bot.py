import telegram
from telegram.ext import Updater, CommandHandler
import requests
import json
from datetime import datetime
import pytz

### Telegram bot setup

updater = Updater(token="406484014:AAH0ik5seLM0bI07aUY78kMMiZaPuCtLAyA")
bot = telegram.Bot(token="406484014:AAH0ik5seLM0bI07aUY78kMMiZaPuCtLAyA")
dispatcher = updater.dispatcher

### GET request for Fixtures from football-data.org

url = "http://api.football-data.org/v2/fixtures/"
querystring = {"league":"PL","timeFrame":"n7"}
headers = {
    'x-auth-token': "0c0d4ed2886a44bfa2434fe958103dac",
    'x-response-control': "minified",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
response_json = json.loads(response.text)

### GET request for Table from football-data.org

url2 = "http://api.football-data.org/v2/competitions/445/leagueTable"
headers2 = {
    'x-auth-token': "0c0d4ed2886a44bfa2434fe958103dac",
    'x-response-control': "minified",
    'cache-control': "no-cache"
    }

response2 = requests.request("GET", url2, headers=headers2)
response_json2 = json.loads(response2.text)

### Fixture list from GET request

def result(input):
    
    local_timezone = pytz.timezone("Asia/Singapore")

    str_print = "== Upcoming Fixtures ==\n\n"

    for i in input["fixtures"]:

        ## convert datetime to local time

        time = (datetime.strptime(i["date"], "%Y-%m-%dT%H:%M:%SZ")).replace(tzinfo=pytz.utc).astimezone(local_timezone)

        str_print += i["homeTeamName"] + " v " + i["awayTeamName"] + "\nDate: " + str(time.replace(tzinfo=None))[:10] \
                     + "\nKickoff: " + str(time.replace(tzinfo=None))[11:16] + "\n\n"

    return str_print

### Table from GET request

def result2(input):

    table1 = "# | Team (Pts)\n-----------------------\n"

    for i in response_json2["standing"]:
        table1 += "{} {} ({})\n".format(str(i["rank"]), i["team"].replace("ManU", "Man United"), str(i["points"]))

    return table1

### Bot command functions

def start(bot, update):

    bot.send_message(chat_id=update.message.chat_id, text="Bot started!")

def fixture(bot, update):

    bot.send_message(chat_id=update.message.chat_id, text=result(response_json))

def table(bot,update):

    bot.send_message(chat_id=update.message.chat_id, text=result2(response_json2))

### Main section - bot commands

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

fixture_handler = CommandHandler('fixture', fixture)
dispatcher.add_handler(fixture_handler)

table_handler = CommandHandler('table', table)
dispatcher.add_handler(table_handler)

updater.start_polling()

## Make sure bot is running

print()
print("Running...")
print()
print()