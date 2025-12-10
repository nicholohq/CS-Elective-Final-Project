import requests

BASE_URL = "http://127.0.0.1:5000/operators"
LOGIN_URL = "http://127.0.0.1:5000/login"

def print_response(title, response):
    print(f"\n=== {title} ===")
    print("Status Code:", response.status_code)
    try:
        print(response.json())
    except Exception:
        print(response.text)

login_data = {"username": "admin", "password": "admin123"}
login_resp = requests.post(LOGIN_URL, json=login_data)
if login_resp.status_code == 200:
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Logged in, token received")
else:
    print("❌ Login failed")
    headers = {}

formats = ["json", "xml"]

for fmt in formats:
    response = requests.get(f"{BASE_URL}?format={fmt}")
    print_response(f"GET all operators ({fmt.upper()})", response)

new_operator = {
    "operator_name": "Lee",
    "class": "Specialist",
    "subclass": "Merchant"
}
response = requests.post(BASE_URL, json=new_operator, headers=headers)
print_response("POST a new operator", response)
new_id = response.json().get("id")

if new_id:
    for fmt in formats:
        response = requests.get(f"{BASE_URL}/{new_id}?format={fmt}")
        print_response(f"GET operator by ID {new_id} ({fmt.upper()})", response)

update_data = {
    "operator_name": "Ch'en the Holungday",
    "class": "Sniper",
    "subclass": "Spreadshooter"
}
response = requests.put(f"{BASE_URL}/{new_id}", json=update_data, headers=headers)
print_response(f"PUT (update) operator ID {new_id}", response)

response = requests.delete(f"{BASE_URL}/{new_id}", headers=headers)
print_response(f"DELETE operator ID {new_id}", response)

for fmt in formats:
    response = requests.get(f"{BASE_URL}?format={fmt}")
    print_response(f"GET all operators after deletion ({fmt.upper()})", response)

search_queries = [
    {"name": "Saria"},
    {"class": "Sniper"},
    {"subclass": "Healer"}
]

for query in search_queries:
    for fmt in formats:
        response = requests.get(f"{BASE_URL}/search", params={**query, "format": fmt})
        print_response(f"SEARCH {query} ({fmt.upper()})", response)
