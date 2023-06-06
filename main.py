import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 30.4189  # Your latitude
MY_LONG = 4.2338  # Your longitude
MY_EMAIL = "learnpythn@gmail.com"
PASSWORD = "yfhazrrcqelsqraa"
my_position = MY_LAT + MY_LONG


def get_latest_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    print(data)
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
#Your position is within +5 or -5 degrees of the ISS position.
    iss_position = iss_longitude + iss_latitude
    print(iss_latitude)
    print(iss_longitude)
    return iss_position

# Parameters from the api sunrise-sunset.org
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
hour_now = time_now.hour


# If the ISS is close to my current position
def check_position():
    iss_position = get_latest_iss_position()
    if (my_position + 5) >= iss_position >= (my_position - 5) and hour_now >= sunset:
        print("masuk")
        with smtplib.SMTP(host="smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Alert!!!\n\nLook up, the space station is above your head")


start_time = time.time()
while True:
    check_position()
    time.sleep(60.0)