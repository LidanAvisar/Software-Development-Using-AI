import requests
from joblib import Parallel, delayed
import random

azure_server_url = "https://my-containerapp.jollyforest-8bfb57eb.eastus.azurecontainerapps.io/process_event/"

userids = ["12345", "user2", "user3", "user4", "user5"]
eventnames = ["testevent", "event2", "event3", "event4", "event5"]

def make_request(url, userid, eventname):
    event_data = {
        "userid": userid,
        "eventname": eventname
    }
    response = requests.post(url, json=event_data)

    with open('request_log.txt', 'a') as file:
        file.write(f"UserID: {userid}, EventName: {eventname}, Status Code: {response.status_code}\n")
    return response.status_code

if __name__ == "__main__":
    num_requests = 1000

    results = Parallel(n_jobs=-1)(delayed(make_request)(azure_server_url, random.choice(userids), random.choice(eventnames)) for _ in range(num_requests))

    successful_requests = sum(1 for status_code in results if status_code == 200)

    print(f"Total successful requests: {successful_requests}")
