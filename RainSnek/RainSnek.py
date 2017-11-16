import discord
import json, re, requests

#Example: http://api.wunderground.com/api/dca6949ac57f1267/geolookup/conditions/q/NC/charlotte.json
rest_url = 'http://api.wunderground.com/api/'
client = discord.Client()

'''
    Planned features:
    New_york can be typed New York when being searched
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


def fetch_weather(state = 'NC', city = 'charlotte'):
    print("Fetching weather from " + city + ", " + state)
    r = requests.get(rest_url + globalVars.apiKeys["wunderground"] + "/forecast/conditions/q/" 
                     + state.replace(" ", "_") + "/" + city.replace(" ", "_") + ".json")
    return r.json()

def wInfoLong(state = 'NC', city = 'charlotte'):
    return

def wInfoShort(state = 'NC', city = 'charlotte'):
    message = fetch_weather(state, city)
    try:
        fLocation = message['current_observation']['display_location']['full']
        fTemp = str(message['current_observation']['temp_f']) + "°F but feels like " + str(message['current_observation']['feelslike_f']) + "°F"
        fWeather = message['current_observation']['weather'] + " with a " + message['forecast']['txt_forecast']['forecastday'][0]['pop'] + "% chance of rain right now."
        return  fLocation + " is currently " + fTemp + ".\nIt's " + fWeather
    except:
        print(str(message))
        return "Error, I couldnt find: " + str(state) + " or " + str(city)

def weatherIn(message = ""):
    city = re.findall('weather in (.*)[$|\s]', message)[0]

    try:
        state = re.findall(('weather in ' + city + ' (.*)'), message)[0]
    except:
        state = 'NC'

    return wInfoShort(state, city)

@client.event
async def on_message(message):
    if message.content.startswith('<@' + client.user.id + ">"):
        command = message.content.split('<@' + client.user.id + ">")[1].strip().rstrip()
        if 'weather' in command and 'in' not in command:
            await client.send_message(message.channel, wInfoShort())
        elif 'weather in' in command:
            await client.send_message(message.channel, weatherIn(command))
    if 'weather in' in message.content:
        await client.send_message(message.channel, weatherIn(command))
    
    if 'the weather' in message.content or 'weather right now' in message.content:
        await client.send_message(message.channel, wInfoShort())

def main():
    #print(wInfoShort())

    client.run(globalVars.apiKeys['discord'])
    print("Online")
    return

if __name__ == '__main__':
    loadKeys()
    main()