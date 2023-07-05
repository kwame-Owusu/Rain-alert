from datetime import *
import os
import requests
from twilio.rest import Client


# this is an example on how API should be written, its much cleaner than putting everything in the response call.
API_KEY = "60ec27ddc046a414b4a1c9cb4aa02939"
OWM_endpoint = "https://api.openweathermap.org/data/2.5/weather?"

ACCOUNT_SID =  os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN =  os.environ['TWILIO_AUTH_TOKEN']



weather_parameters  ={
    "lat": 35.181446,
    "lon": 136.906403,
    "appid": API_KEY,

}
 

response = requests.get(OWM_endpoint, params=weather_parameters)
condition_code = response.json()["weather"][0]["id"]
main_weather = (response.json()["weather"][0]["main"])
weather_description = (response.json()["weather"][0]["description"])
# temp was in kelvin so had to subtract 273.15 for celcius metric
celcius = round(response.json()["main"]["feels_like"] - 273.15, 2)

# change datetime from utc to GMT
time_utc = response.json()["dt"]
time_GMT = datetime.utcfromtimestamp(time_utc).strftime('%m-%d-%Y %H:%M:%S')


will_rain = False
if int(condition_code) < 700:
    will_rain = True

if will_rain:
    # implementation of the twilio API
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message  = client.messages.create \
        (
        body=f"OWN weather code: {condition_code},weather: {main_weather}, description: {weather_description}, temp:{celcius}, at time: {time_GMT}, its going to rain, take an umbrella ☔",
        from_="+447723473934",
        to="+447577931272"
    )
    print(message.status)




