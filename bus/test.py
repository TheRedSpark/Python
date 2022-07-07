import dvb
import time

origin = 'Zellescher Weg'
city_origin = 'Dresden'
destination = 'Postplatz'
city_destination = 'Dresden'
time = int(time.time()) # a unix timestamp is wanted here
deparr = 'dep'  # set to 'arr' for arrival time, 'dep' for departure time

dvb.route(origin, destination, city_origin, city_destination, time, deparr)