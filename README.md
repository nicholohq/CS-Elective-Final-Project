# CSE-Final-Project
Arknights REST API by Nicholo Luigi P. Dela Rosa

# 🧩 Operators API (Flask + MySQL)

A simple REST API built with Flask and MySQL that manages game operators (name, class, subclass).
It supports CRUD operations, search, JWT authentication, and JSON/XML response formats.

# 📦 Project Features

- ✅ Get all operators
- ✅ Get operator by ID
- ✅ Add new operator (JWT protected)
- ✅ Update operator (JWT protected)
- ✅ Delete operator (JWT protected)
- ✅ Search by name, class, or subclass
- ✅ JSON and XML response formats via URL parameter

# 📦 Packages Used
- Python 3
- Flask
- Flask-JWT-Extended
- Flask-MySQLdb
- Flask-Bcrypt/bcrypt
- dicttoxml
- mysqlclient
- requests
- Werkzeug
- Jinja2

# Installation 
### Step 1: Clone Repository
```
git clone https://github.com/nicholohq/CSE-Final-Project.git
cd arknights_api
```

---

### Step 2: Create Virtual Environment
```
python -m venv venv
```

Activate
```
venv\Scripts\activate
```
---

### Step 3: Install dependencies
```
pip install -r requirements.txt
```
---

### Step 4: MySQL Database Setup


#### - Option 1: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Click Server -> Data Import
4. Select Import from Self-Contained File
5. Choose the file: dela_rosa.sql
6. Click Start Import


#### - Option 2: Using Terminal
1. Open Command Prompt or Terminal and run:
```
mysql -u root -p
```
Then inside MYSQL:
```
CREATE DATABASE arknights;
USE arknights;
SOURCE dela_rosa.sql;
```
---

### Step 5: Configure Database Connection
Open config.py and make sure it matches your MySQL setup:
```
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "arknights"
```

---

### Step 6: Run the API Server
In your project folder, run:
```
python app.py
```

# Example Requests & Responses

## 1. Get all Operators

### Response (JSON)
GET /operators?format=json
```
[
  {"id":1,"operator_name":"eyjafjalla","class":"caster","subclass":"core"},
  {"id":2,"operator_name":"saria","class":"defender","subclass":"guardian"}
]
```
### Response (XML)
GET /operators?format=xml
```
<operators>
  <item><id>1</id><operator_name>eyjafjalla</operator_name><class>caster</class><subclass>core</subclass></item>
  <item><id>2</id><operator_name>saria</operator_name><class>defender</class><subclass>guardian</subclass></item>
</operators>
```

## 2. Get operator by ID
GET /operators/1?format=json
```
{"id":1,"operator_name":"eyjafjalla","class":"caster","subclass":"core"}
```

## 3. POST new operator (JWT required)
POST /operators
Request JSON:
```
{"operator_name":"Lee","class":"Specialist","subclass":"Merchant"}
```
Response JSON:
```
{"message":"Operator added","id":35}
```

## 4. PUT update operator (JWT required)
PUT /operators/35
Request JSON:
```
{"operator_name":"Ch'en","class":"Sniper","subclass":"Spreadshooter"}
```
Response JSON:
```
{"message":"Operator updated"}
```


## 5. DELETE operator (JWT required)
DELETE /operators/35
Response JSON:
```
{"message":"Operator deleted"}
```

## 6. SEARCH operators
GET /operators/search?name=Saria&format=json
Response JSON:
```
[{"id":2,"operator_name":"saria","class":"defender","subclass":"guardian"}]
```
