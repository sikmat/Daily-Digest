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
                search = (input('Please input city: '))
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
    pass

if __name__ == '__main__':
    # test code
    print('\nTesting quote generation..')

    quote = get_random_quote()
    print(f' - Random quote is "{quote["quote"]}" - {quote["author"]}')

    quote = get_random_quote(quotes_file= None)
    print(f' - Default quote is "{quote["quote"]}" - {quote["author"]}')

    print('\nTesting weather forecasting..')

    get_weather_forecast()
    get_twitter_trends()