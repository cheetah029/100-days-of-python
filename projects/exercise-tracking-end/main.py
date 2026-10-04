import requests
from datetime import datetime
import os

GENDER = None
WEIGHT_KG = None
HEIGHT_CM = None
AGE = None

APP_ID = os.environ["NT_APP_ID"]
API_KEY = os.environ["NT_API_KEY"]

NUTRITIONIX_API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEET_API_ENDPOINT = os.environ["SHEET_API_ENDPOINT"]

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(NUTRITIONIX_API_ENDPOINT, json=parameters, headers=headers)
result = response.json()

bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
}

today_date = datetime.now().strftime("%m/%d/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(SHEET_API_ENDPOINT, json=sheet_inputs, headers=bearer_headers)

    print(sheet_response.text)
