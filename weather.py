import requests
import re
from secrets import API_KEY


def main():
    while True:
        zip_code = input("Please enter a five digit zip code: ").strip()
        try:
            int(zip_code)
        except ValueError:
            print("Please enter a valid zip code.")
        else:
            if re.match(r'^\d{5}', zip_code):
                print(WeatherReport(zip_code))
            else:
                print("Please enter a valid zip code.")
                continue
        again = input("Enter 'z' to search again, any key to exit: ").lower()
        if again != 'z':
            break


class WeatherReport(object):
    def __init__(self, zip_code):
        self.zip_code = zip_code
        self.base_url = "http://api.wunderground.com/api/{}/conditions/forecast10day/astronomy/alerts/currenthurricane/q/{}.json".format(API_KEY, zip_code)
        json = requests.get(self.base_url).json()
        
        # CONDITIONS
        conditions = json['current_observation']
        self.location = conditions["display_location"]["full"]
        self.weather = conditions["weather"]
        self.temp = conditions["temp_f"]

        # 10 DAY FORECAST
        ten_day = json['forecast']['txt_forecast']['forecastday']
        self.ten_day = [(day['title'], day['fcttext']) for day in ten_day]

        # SUNRISE/SUNSET
        sunrise = json['sun_phase']['sunrise']
        sunset = json['sun_phase']['sunset']
        self.sunrise = "{}:{}".format(sunrise['hour'], sunrise['minute'])
        self.sunset = "{}:{}".format(sunset['hour'], sunset['minute'])

        # WEATHER ALERTS
        alerts = json['alerts']
        self.alerts = [(alert['description'],
                        alert['expires']) for alert in alerts]

        # HURRICANES
        hurs = json['currenthurricane']
        self.hurricanes = [hur['stormInfo']['stormName_Nice'] for hur in hurs]

    def __str__(self):
        text = "TODAY IN {}:\n".format(self.location.upper())
        text += 'Weather: {}\nTemperature: {}\n'.format(self.weather,
                                                        self.temp)
        text += "Sunrise: {}\nSunset: {}\n".format(self.sunrise, self.sunset)
        for alert in self.alerts:
            text += "Alert: {}; Expires: {}\n".format(alert[0], alert[1])

        text += "\nTEN DAY FORECAST:\n"
        for day in self.ten_day:
            text += "{}: {}\n".format(day[0], day[1])

        text += '\nHURRICANES IN THE WORLD RIGHT MEOW:\n'
        for hur in self.hurricanes:
            text += "{}\n".format(hur)

        return text


if __name__ == "__main__":
    main()
