import os
import requests
from twilio.rest import Client

twilio_phone_num = os.environ['twilio_phone_num']
my_phone_num = os.environ['my_phone_num']
account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']

API_KEY = os.environ['API_KEY']
LAT = 40
LON = 122
parameters = {
    'lat': LAT,
    'lon': LON,
    'appid': API_KEY,
}

response = requests.get(url='https://api.openweathermap.org/data/2.5/forecast', params=parameters)
response.raise_for_status()
weather_data = response.json()

will_rain: bool = False

weather_list = weather_data['list']
for hour_interval in weather_list[:12]:
    weather_id = hour_interval['weather'][0]['id']
    print(weather_id)
    if weather_id < 1000:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="There is no rain in Redding, CA right now",
            from_=twilio_phone_num,
            to=my_phone_num
        )
    print(message.status)
