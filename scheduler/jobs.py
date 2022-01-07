from django.conf import settings
import requests
import json
import random
from base.models import NewUser
from base.email import send_happy_birthday
from datetime import datetime

postcodes = [
	"SW1A 1AA",
	"PE35 6EB", 
	"CV34 6AH",
	"EH1 2NG"
]

# def schedule_api():

# 	postcode = postcodes[random.randint(0, 3)]

# 	full_url = f"https://api.postcodes.io/postcodes/{postcode}"
			
# 	r = requests.get(full_url)
# 	if r.status_code == 200:

# 		result = r.json()["result"]

# 		lat = result["latitude"]
# 		lng = result["longitude"]

# 		print(f'Latitude: {lat}, Longitude: {lng}')

		#77779

def schedule_api():
  try:
    today = datetime.today().strftime('%Y-%m-%d')
    users = NewUser.objects.all()
    for user in users:
      if str(user.birthday) == today:
        send_happy_birthday(user.user_name, user.email) 
      else:
        pass
        # message = {'detail':'Your new password has been sent your email'}
  except:
    message = {'detail':'User does not exist'}
    print(message)
   