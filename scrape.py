import json
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

totalProfiles = 100
users = []
session = FuturesSession()

for i in range(totalProfiles/100):
  data = requests.get("https://www.roblox.com/search/users/results?keyword=fortnite&maxRows=100&startIndex=" + str(i*100)).json()
  # print(data)

  totalProfiles = data["TotalResults"]

  profileRequests = {}
  for user in data["UserSearchResults"]:
    userUrl = user["UserProfilePageUrl"]
    profileRequests[user["UserId"]] = session.get("https://roblox.com"+userUrl)
    

  for user in data["UserSearchResults"]:
    html = BeautifulSoup(profileRequests[user["UserId"]].result().text, "html.parser")
    date = html.find("p", attrs={"class": "text-lead"}).text.split("P")[0]

    users.append({
      "name": user["Name"],
      "id": user["UserId"],
      "date": date
    })

    print("Profile " + str(user["UserId"]) + ": " + date)

with open('data.json', 'w') as outfile:
    json.dump(users, outfile)