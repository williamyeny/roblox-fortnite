import json
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

session = FuturesSession()

searchUrl = "https://www.roblox.com/search/users/results?keyword=fortnite"
totalResults = session.get(searchUrl).result().json()["TotalResults"]

# clear/new file
with open("data.json", "w") as outfile:
  outfile.write("[")

for i in range(totalResults/100):
  users = []
  data = session.get(searchUrl + "&maxRows=100&startIndex=" + str(i*100)).result().json()

  print("[Index " + str(i*100) + " out of " + str(totalResults) + " profiles]")

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

  with open("data.json", "a") as outfile:
    outfile.write(json.dumps(users)[1:-1]) # remove brackets
    if i+1 < totalResults/100:
      outfile.write(",") # add trailing slash if not last
    else:
      outfile.write("]") # add ] if it is

  print("JSON dumped")

