import requests
import datetime
import smtplib
from math import radians, cos, sin, asin, sqrt
import time


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


date = datetime.datetime.now()
latitude = YOUR LOCATION LATITUDE
longitude = YOUR LOCATION LONGITUDE

center_point = [{
    'lat': latitude,
    'lng': longitude
}]

parameters = {
    "lat": latitude,
    "lng": longitude,
    "date": date.date(),
    "formatted": 0
}

# get sunrise/sunset time for the current date and global position based on latitude and longitude
sunrise_sunset_time = requests.get(url=f"https://api.sunrise-sunset.org/json", params=parameters)
sunrise_sunset_time.raise_for_status()

# extract sunrise time and sunset time from the request
sunrise = sunrise_sunset_time.json()["results"]["sunrise"]
sunset = sunrise_sunset_time.json()["results"]["sunset"]

# extract the hour from the sunrise/sunset time
sunrise = int(sunrise.split("T")[1].split(":")[0])
sunset = int(sunset.split("T")[1].split(":")[0])

# get the current time and extract the hour
current_time = int(date.time().hour)

iss_location = requests.get(url="http://api.open-notify.org/iss-now.json")

iss_location = iss_location.json()["iss_position"]

radius = 10
# check if currently it is after sunset or before sunrise

while True:
    time.sleep(60)
    if current_time >= sunset or current_time <= sunrise:
        distance = haversine(float(latitude), float(longitude), float(iss_location["latitude"]),
                             float(iss_location["longitude"]))
        if distance < radius:
            with smtplib.SMTP_SSL(host="smtp.gmail.com") as email:
                email.login(user="SENDER EMAIL", password="SENDER PASSWORD")
                email.sendmail(from_addr="SENDER EMAIL",
                               to_addrs="YOUR EMAIL",
                               msg=f"Subject:The ISS is near you!\n\n"
                                   f"The International Space Station is currently within {distance} km from you!")
    else:
        print("Not here yet...")
