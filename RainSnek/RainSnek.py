import discord
from beautifultable import BeautifulTable
import json, re, requests
import os
from io import BytesIO

#Example: http://api.wunderground.com/api/dc<key>7f1267/geolookup/conditions/q/NC/charlotte.json
rest_url = 'http://api.wunderground.com/api/'
defaultCity = 'Charlotte'
defaultState = 'NC'
version = '1.26.1'

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

def reloadFile():
    print("Reloading the file")
    fileName = "RainSnek.py"

    r = requests.get(globalVars.apiKeys["fileUrl"])

    os.remove(fileName)

    with open(fileName, "wb") as f: 
        f.write(r.content)

    if (os.stat(fileName).st_size >= 100):
        return True
    return False

def fetch_weather(state = defaultState, city = defaultCity):
    print("Fetching weather from " + city + ", " + state)
    r = requests.get(rest_url + globalVars.apiKeys["wunderground"] + "/forecast/conditions/q/" 
                     + state.replace(" ", "_") + "/" + city.replace(" ", "_") + ".json")
    return r.json()

def fetch_radar(state = defaultState, city = defaultCity):
    print("Fetching weather from " + city + ", " + state)
    r = requests.get(rest_url + globalVars.apiKeys["wunderground"] + "/animatedradar/q/" 
                     + state.replace(" ", "_") + "/" + city.replace(" ", "_") + ".gif?newmaps=1&timelabel=1&timelabel.y=10&num=15&delay=25")
    return BytesIO(r.content)

def fetch_sat(state = defaultState, city = defaultCity):
    print("Fetching weather from " + city + ", " + state)
    r = requests.get(rest_url + globalVars.apiKeys["wunderground"] + "/animatedsatellite/q/" 
                     + state.replace(" ", "_") + "/" + city.replace(" ", "_") + ".gif?newmaps=1&timelabel=1&timelabel.y=10&num=15&delay=25")
    return BytesIO(r.content)

def fetch_alerts(state = defaultState, city = defaultCity):
    print("Fetching weather from " + city + ", " + state)
    r = requests.get(rest_url + globalVars.apiKeys["wunderground"] + "/alerts/q/" 
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
            if 'Night' not in time['title']:
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

def wInfoAlert(state = defaultState, city = defaultCity):
    message = fetch_alerts(state, city)
    try:
        resp = ''
        for alert in message['alerts']:
            resp += alert['description'] + '\n' + alert['date'] + '\n' + alert['message'].split('\n\n\n')[0]
            resp += '\n'
        return resp
    except:
        print(str(message))
        return "Error, I couldnt find: " + str(state) + " or " + str(city)

def wInfoTodayRadar(state = defaultState, city = defaultCity):
    try:
        return fetch_radar(state, city)
    except:
        print("RADAR ERROR")
        return "Error, I couldnt find: " + str(state) + " or " + str(city)

def wInfoTodaySat(state = defaultState, city = defaultCity):
    try:
        return fetch_sat(state, city)
    except:
        print("RADAR ERROR")
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
    await client.change_presence(game=discord.Game(name='Counting Clouds'))


@client.event
async def on_message(message):
    if message.content.startswith('<@' + client.user.id + ">"):
        await client.send_typing(message.channel)
        command = message.content.split('<@' + client.user.id + ">")[1].strip().rstrip().lower()
        if 'weather in' in command:
            await client.send_message(message.channel, weatherIn(command))
        elif ('weather alert' in command):
            await client.send_message(message.channel, wInfoAlert())
        elif 'weather' in command:
            await client.send_message(message.channel, wInfoShort())
            if ('tonight' in command):
                await client.send_message(message.channel, wInfoNextTwo())
            elif ('week' in command):
                await client.send_message(message.channel, wInfoFullThree())
            elif ('today' in command):
                await client.send_message(message.channel, wInfoNextTwo())
        elif ('the high' in command or 'the low' in command):
            await client.send_message(message.channel, wInfoTodayHL())
        elif ('radar' in command):
            await client.send_file(message.channel, wInfoTodayRadar() ,filename='Radar_image.gif')
        elif ('satellite' in command or 'sat' in command):
            await client.send_file(message.channel, wInfoTodaySat() ,filename='Sat_image.gif')
        elif ('weather alert' in command):
            await client.send_message(message.channel, wInfoAlert())
        elif ('version' in command):
            await client.send_message(message.channel, version)
        elif ('reload' in command and message.author.id == globalVars.apiKeys["ownerid"]):
            await client.send_message(message.channel, "Restarting...")
            if reloadFile():
                quit()
            else:
                await client.send_message(message.channel, "Update Failed")
        else:
            await client.send_message(message.channel, "Hello friend")
        return

    formattedMessage = message.content.lower()

    if 'weather in' in formattedMessage:
        await client.send_typing(message.channel)
        await client.send_message(message.channel, weatherIn(formattedMessage))
    elif ('weather alert' in formattedMessage) and 'see' not in formattedMessage:
        await client.send_typing(message.channel)
        await client.send_message(message.channel, wInfoAlert())
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
    elif ('weather radar' in formattedMessage) and 'see' not in formattedMessage:
        await client.send_typing(message.channel)
        await client.send_file(message.channel, wInfoTodayRadar() ,filename='Radar_image.gif')
    elif ('weather sat' in formattedMessage) and 'see' not in formattedMessage:
        await client.send_typing(message.channel)
        await client.send_file(message.channel, wInfoTodaySat() ,filename='Sat_image.gif')

def main():
    #print(wInfoShort())'
    client.run(globalVars.apiKeys['discord'])

if __name__ == '__main__':
    loadKeys()
    main()