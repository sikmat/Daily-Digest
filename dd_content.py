import csv
import random
from urllib import request
import json
from _datetime import datetime
import requests
import tweepy

"""
Retrieve a random quote from the specified CSV file.
"""
def get_random_quote(quotes_file='quotes.csv'):
    try: # Loading quotes from csv file
        with open(quotes_file) as csvfile:
            quotes = [{'author': line[0],
                       'quote': line[1]} for line in csv.reader(csvfile, delimiter='|')]
    except Exception as e: # use a default quote, just in case
        quotes = [{'author': 'Eric Idle',
                   'quote': 'Always look on the bright side of life.'}]

    return random.choice(quotes)

"""
Retrieve the current weather forecast from OpenWeatherMap.
"""
def get_weather_forecast():
    api_key = '6c668188b018460ce70a7fedc6548bb8'
    api_call = f'https://api.openweathermap.org/data/2.5/forecast?appid={api_key}&units=metric'

    running = True
    time_stamp = datetime.now()
    current_time = time_stamp.strftime("%H:%M:%S")
    print("Time:", current_time)

    # Program loop
    while running:
        while True:
            try:
                search = 'Cape Town' #(input('Please input city: '))
            except ValueError:
                print("Sorry, I didn't understand that.")
            else:
                if search != '':
                    city = search
                    if city.lower() == 'sf':
                        city = 'San Francisco, US'
                    api_call += '&q=' + city
                    break

                else:
                    print('{} is not a valid option.'.format(search))

        # Stores the Json response
        json_data = requests.get(api_call).json()

        location_data = {
            'city': json_data['city']['name'],
            'country': json_data['city']['country']
        }
        print('\n{city}, {country}'.format(**location_data))

        current_date = ''
        for item in json_data['list']:
            time = item['dt_txt']

            next_date, hour = time.split(' ')

            if current_date != next_date:
                current_date = next_date
                year, month, day = current_date.split('-')
                date = {'y': year, 'm': month, 'd': day}
                print('\n{m}/{d}/{y}'.format(**date))

            hour = int(hour[:2])
            if hour < 12:
                if hour == 0:
                    hour = 12
                m = 'AM'
            else:
                if hour > 12:
                    hour -= 12
                m = 'PM'
            print('\n%i:00 %s' % (hour, m))

            temperature = item['main']['temp']
            description = item['weather'][0]['description'],
            print('Weather condition: %s' % description)
            print('Temperature: {:.2f}'.format(temperature))

            running = False


def get_twitter_trends():

    consumer_key = "oRRvbgOVHHk4lYvZIECQHU20R"  # api_key
    consumer_secret = "qwNh9smJS3vmlZd5ym8Rs4gAwsRb3f7ivjLgJkaL55t4iconax"  # api_key_secret
    access_token = "1774478928377151488-EIPUfDWJZBL3TB7Mm0DfHBl2Uug3Ct"
    access_token_secret = "SBKzIc7EuJAwTYwk8gJVvexEWNT34CmYZVFXkFU8bpILg"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    woeid = input('Please provide WOEID :')
    trends = api.get_place_trends(woeid)
    print("The top trends for the location are :")

    for value in trends:
        for trend in value['trends']:
            print(trend['name'])


def get_wikipedia_article():
    url = 'https://en.wikipedia.org/api/rest_v1/page/random/summary/'

    headers = {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJkZmZmNWYzMzliNDlmYzBmZWRjNzBkZWQxY2QwMWE4YiIsImp0aSI6ImQ0NTlmMGI0YzE0NTc4ZDA0MmRkNTFjMDlmNDY1YzQ2Zjk5MGYzNTg4NWYyODc1MmRlYTA0Y2EyOGEzOWRkNWQ0M2I2ZDc2NjQwZWMwMjYzIiwiaWF0IjoxNzExOTg1NzEyLjg5MTksIm5iZiI6MTcxMTk4NTcxMi44OTE5MDQsImV4cCI6MzMyNjg4OTQ1MTIuODkwMjc4LCJzdWIiOiI3NTMzMTIxNSIsImlzcyI6Imh0dHBzOi8vbWV0YS53aWtpbWVkaWEub3JnIiwicmF0ZWxpbWl0Ijp7InJlcXVlc3RzX3Blcl91bml0Ijo1MDAwLCJ1bml0IjoiSE9VUiJ9LCJzY29wZXMiOlsiYmFzaWMiXX0.CUhgcnnps-4_TC3AIwBJDdLN84LB9lQuoC2ivt2IuVwPJq9ldBWrIbkZeySFwK3ESW4zQE2PSUyWYBqiMi6ii76rAA_Grere8fGKXiqP6DtuR_oUbRpk8c0pY1GGSSJe59Qk9kcGlhtwl7E22vfUUefpnFuYq2nJjYBJ7G7lxGxXsRcxPlRAJiYRlLNYhEibnH1rVkr10lop_qbEz_x_e9vgnmhu-2aWpbIDJhlVSlta1BysBIeoniwRiMsvfF9EEpO-336Zq9Iy_-RmzDcjmPinnuwUaM9trXd8fVMI--ncdQKeX1gnHpb0QdtdbCDhS7Z-4E2avYfMRGi-aHt0eTqHjfH-412JsuBLHJSju-E3wqbCx4ZA1vn6dBNfqNzrPMzvUjxeqg-da1Tvl1EkNliJfjJ1323VMPv5coEVBrzZzSz4T36U--JFLb0m6I6bOdK3XXm3bJ7Z9DN8MPAT-OF8FQkMDMZy1tKPzxnr3O2W4r87j4jIXam3dbKLD2XKhUu_4hcSMaMNstSKk_rBaiKV1d1RcNJllik6n5yUl5l6LFL4Qkuko-zkfrpihJL2qT-S2iNw1D4869ap5cuyvqFhrbW7Ebu2lbfJb_nQ_U9hP4mt6VxIA8-wbTeUfQ18nsdetxWQRuL27JlHLqVmIIcZL2bT0Mg5H0UDm3rgmgI',

        'User-Agent': 'Daily DIgest (sikelelamathole.sm@gmail.com)'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    title = data['title']
    extract = data['extract']
    timestamp = data['timestamp']
    print(title, timestamp)
    print(extract)
    # print(data)

if __name__ == '__main__':
    # test code
    print('\nTesting Random Quote generation..')

    quote = get_random_quote()
    print(f' - Random quote is "{quote["quote"]}" - {quote["author"]}')

    quote = get_random_quote(quotes_file= None)
    print(f' - Default quote is "{quote["quote"]}" - {quote["author"]}')

    print('\nTesting Weather Forecasting..')
    get_weather_forecast()

    #get_twitter_trends()

    print('\nTesting Wikipedia Article...')
    get_wikipedia_article()