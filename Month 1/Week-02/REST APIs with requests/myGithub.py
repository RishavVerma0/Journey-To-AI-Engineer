import requests

# Your GitHub details
USERNAME = "RishavVerma0"
REPO = "Journey-To-AI-Engineer"
TOKEN = "your_personal_access_token"

# GitHub API URL
url = f"https://api.github.com/repos/{USERNAME}/{REPO}"

# Headers for authentication
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Send GET request
response = requests.get(url, headers=headers)

# Check response
if response.status_code == 200:
    repo_data = response.json()

    print("Repository Name:", repo_data["name"])
    print("Description:", repo_data["description"])
    print("Stars:", repo_data["stargazers_count"])
    print("Forks:", repo_data["forks_count"])
    print("URL:", repo_data["html_url"])

else:
    print("Error:", response.status_code)
    print(response.json())