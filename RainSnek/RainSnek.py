import discord
from beautifultable import BeautifulTable
import json, re, requests

#Example: http://api.wunderground.com/api/dc<key>7f1267/geolookup/conditions/q/NC/charlotte.json
rest_url = 'http://api.wunderground.com/api/'
defaultCity = 'Charlotte'
defaultState = 'NC'

client = discord.Client()
'''
    Planned features:
    5 day forcasts
'''


class globalVars:
    def __init__(self, apiKeys = dict()):
        self.apiKeys = apiKeys

def loadKeys():
    #Loads two api keys under the values discord and wunderground
    with open('apiKeys.json') as data:    
        globalVars.apiKeys = json.load(data)
    print("Loaded API keys")


def fetch_weather(state = defaultState, city = defaultCity):
    print("Fetching weather from " + city + ", " + state)
    r = requests.get(rest_url + globalVars.apiKeys["wunderground"] + "/forecast/conditions/q/" 
                     + state.replace(" ", "_") + "/" + city.replace(" ", "_") + ".json")
    return r.json()

def wInfoLong(state = defaultState, city = defaultCity):
    return

def wInfoShort(state = defaultState, city = defaultCity):
    message = fetch_weather(state, city)
    try:
        fLocation = message['current_observation']['display_location']['full']
        if (str(message['current_observation']['temp_f']) == str(message['current_observation']['feelslike_f'])):
            fTemp = str(message['current_observation']['temp_f']) + "°F"
        else:
            fTemp = str(message['current_observation']['temp_f']) + "°F and feels like " + str(message['current_observation']['feelslike_f']) + "°F"
        fWeather = message['forecast']['txt_forecast']['forecastday'][0]['fcttext']
        return  fLocation + " is currently " + fTemp + ".\n" + fWeather
    except:
        print(str(message))
        return "Error, I couldnt find: " + str(state) + " or " + str(city)

def wInfoFullThree(state = defaultState, city = defaultCity):
    message = fetch_weather(state, city)
    try:
        table = BeautifulTable()
        table.column_headers = ["Time","Precip","Forecast"]
        for time in message['forecast']['txt_forecast']['forecastday']:
            table.append_row([time['title'],time['pop'] + '%',time['fcttext']])
        return  str('```' + str(table) + '```')
    except:
        print(str(message))
        return "Error, I couldnt find: " + str(state) + " or " + str(city)

def wInfoNextTwo(state = defaultState, city = defaultCity):
    message = fetch_weather(state, city)
    try:
        table = BeautifulTable()
        table.column_headers = ["Time","Precip","Forecast"]
        for time in message['forecast']['txt_forecast']['forecastday'][:2]:
            table.append_row([time['title'],time['pop'] + '%',time['fcttext']])
        return  str('```' + str(table) + '```')
    except:
        print(str(message))
        return "Error, I couldnt find: " + str(state) + " or " + str(city)

def wInfoTodayHL(state = defaultState, city = defaultCity):
    message = fetch_weather(state, city)
    try:
        table = BeautifulTable()
        table.column_headers = ["High","Low"]
        table.append_row([message['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit'] + '°F', message['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit'] + '°F'])
        return  str('```' + str(table) + '```')
    except:
        print(str(message))
        return "Error, I couldnt find: " + str(state) + " or " + str(city)

def weatherIn(message = ""):

    location = re.findall('weather in (.*)', message)[0].split(" ")

    if len(location) > 1:
        city = location[0]
        
        if len(location) > 2:
            for word in location[1:len(location) - 1]:  
                city += ("_" + word)

        state = location[len(location) - 1]
    else:
        city = location[0]
        state = defaultState

    return wInfoShort(state, city)

@client.event
async def on_ready():
    print("Online")
    await client.change_status(game=discord.Game(name='Counting Clouds'))

@client.event
async def on_message(message):
    if message.content.startswith('<@' + client.user.id + ">"):
        await client.send_typing(message.channel)
        command = message.content.split('<@' + client.user.id + ">")[1].strip().rstrip().lower()
        if 'weather' in command and 'in' not in command:
            await client.send_message(message.channel, wInfoShort())
        elif 'weather in' in command:
            await client.send_message(message.channel, weatherIn(command))
        elif ('tonight' in command and 'in' not in command):
            await client.send_message(message.channel, wInfoNextTwo())
        elif ('this week' in command and 'in' not in command):
            await client.send_message(message.channel, wInfoFullThree())
        elif ('today' in command and 'in' not in command):
            await client.send_message(message.channel, wInfoNextTwo())
        elif ('the high today' in formattedMessage or 'the low today' in formattedMessage) and 'see' not in formattedMessage:
            await client.send_message(message.channel, wInfoTodayHL())
        else:
            await client.send_message(message.channel, "Hello friend")
        return

    formattedMessage = message.content.lower()

    if 'weather in' in formattedMessage:
        await client.send_typing(message.channel)
        await client.send_message(message.channel, weatherIn(formattedMessage))
    elif ('the weather' in formattedMessage or 'weather right now' in formattedMessage) and 'see' not in formattedMessage:
        await client.send_typing(message.channel)
        if ('tonight' in formattedMessage):
            await client.send_message(message.channel, wInfoNextTwo())
        elif ('this week' in formattedMessage):
            await client.send_message(message.channel, wInfoFullThree())
        elif ('today' in formattedMessage):
            await client.send_message(message.channel, wInfoNextTwo())
        else:
            await client.send_message(message.channel, wInfoShort())
    elif ('the high today' in formattedMessage or 'the low today' in formattedMessage) and 'see' not in formattedMessage:
        await client.send_typing(message.channel)
        await client.send_message(message.channel, wInfoTodayHL())

def main():
    #print(wInfoShort())'
    client.run(globalVars.apiKeys['discord'])

if __name__ == '__main__':
    loadKeys()
    print(wInfoTodayHL())
    #main()