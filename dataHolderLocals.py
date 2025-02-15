import requests
import json

api_key = 'Y06NEWPpRTx5e7rm1NF9BySgHj9anr0Lo7X2MnRfzow6eYJfcTC3d4qxYtIaVZ7X	'
#event_keys_train = ['2023iscmp', '2023hiho', '2023txhou', '2023nytr', '2023arc', '2023cur', '2023dal', '2023gal']
event_keys_test = ['2023casf', '2023cala', '2023txsan', '2023txfor']

event_keys_train = ['2023arc', '2023cur', '2023dal', '2023gal']
#event_keys_test = ['2023hop', '2023joh', '2023mil', '2023new']

events_data_train = []
teams_data_train = []

events_data_test = []
teams_data_test = []

base_url = "https://www.thebluealliance.com/api/v3"
for event in event_keys_train:
    endpoint = f"/event/{event}/matches"
    endpoint2 = f"/event/{event}/teams"

    headers = {
        "X-TBA-Auth-Key": api_key,
    }
    response = requests.get(base_url + endpoint, headers=headers)
    response2 = requests.get(base_url + endpoint2, headers=headers)

    if response.status_code != 200 or response2.status_code != 200:
        print(response.status_code)
        print(response2)
        break
    events_data_train = events_data_train + response.json() + ["stop"]
    teams_data_train = teams_data_train + response2.json() + ["stop"]

for event in event_keys_test:
    endpoint = f"/event/{event}/matches"
    endpoint2 = f"/event/{event}/teams"

    headers = {
        "X-TBA-Auth-Key": api_key,
    }
    response = requests.get(base_url + endpoint, headers=headers)
    response2 = requests.get(base_url + endpoint2, headers=headers)

    if response.status_code != 200 or response2.status_code != 200:
        print(response.status_code)
        print(response2)
        break
    events_data_test = events_data_test + response.json() + ["stop"]
    teams_data_test = teams_data_test + response2.json() + ["stop"]


with open("events_data_train_locals.json", "w") as file:
    json.dump(events_data_train, file, indent=4)

with open("teams_data_train_locals.json", "w") as file:
    json.dump(teams_data_train, file, indent=4)


with open("events_data_test_locals.json", "w") as file:
    json.dump(events_data_test, file, indent=4)

with open("teams_data_test_locals.json", "w") as file:
    json.dump(teams_data_test, file, indent=4)


