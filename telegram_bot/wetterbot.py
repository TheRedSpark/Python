import time  # bereits implementiert
import pyowm  # V2.10.0
import variables as v  # eigene

owm = pyowm.OWM(v.api_id)

"""""""""
Main Functions Definition
"""""
def wetter():
    sf = owm.weather_at_place('Dresden,DE')
    weather = sf.get_weather()
    clouds = weather.get_clouds()  # Cloud coverage
    rainatl = weather.get_rain()  # Rain volume
    rainalt2 = str(rainatl)
    rain = rainalt2.replace("{", "").replace("'1h': ", "").replace("}", "")
    snowalt = weather.get_snow()  # Snow volume
    snowalt2 = str(snowalt)
    snow = snowalt2.replace("{", "").replace("'1h': ", "").replace("}", "")
    wind_speedalt = 3.6 * weather.get_wind()['speed']  # Wind direction and speed
    wind_speed = wind_speedalt.__round__(2)
    wind = weather.get_wind()['deg']
    humidity = weather.get_humidity()  # Humidity percentage
    pressure = weather.get_pressure()['press']  # Atmospheric pressure
    temp = weather.get_temperature('celsius')['temp']
    temp_max = weather.get_temperature('celsius')['temp_max']
    temp_min = weather.get_temperature('celsius')['temp_min']
    time_sql = time.strftime("%Y-%m-%d %H:%M:%S")
    general = weather.get_detailed_status()  # Get general status of weather
      # SQL insert
    # time_mail = time.strftime("%d %m %H:%M")
    # sunrise = weather.get_sunrise_time() #Sunrise time (GMT UNIXtime or ISO 8601)
    sunset = weather.get_sunset_time() #Sunset time (GMT UNIXtime or ISO 8601)
    #visibility = weather.get_lastupdate()

    """""""""
    Hier wird die Liste für die returnable gebaut
    """
    weather = [temp,temp_max,temp_min,clouds,general,wind_speed,sunset,rain]
    return weather

"""""""""
Zeit Abruf 
"""
#print(wetter())
