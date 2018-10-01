import requests, json
from bs4 import BeautifulSoup

totalProfiles = 100
users = []

for i in range(totalProfiles/100):
  data = requests.get("https://www.roblox.com/search/users/results?keyword=fortnite&maxRows=100&startIndex=" + str(i*100)).json()
  # print(data)

  totalProfiles = data["TotalResults"]

  for user in data["UserSearchResults"]:
    userUrl = user["UserProfilePageUrl"]

    soup = BeautifulSoup(requests.get("https://roblox.com"+userUrl).text, "html.parser")
    date = soup.find("p", attrs={"class": "text-lead"}).text.split("P")[0]
    print(date)

    users.append({
      "name": user["Name"],
      "id": user["UserId"],
      "url": userUrl,
      "date": date
    })
    break

with open('data.json', 'w') as outfile:
    json.dump(users, outfile)