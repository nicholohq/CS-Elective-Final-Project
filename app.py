from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import Config
from utils import format_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required


app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)
app.config["SECRET_KEY"] = "nicholohq"
jwt = JWTManager(app)

@app.route("/")
def home():
    return {
        "message": "Connected to Operators API!",
        "endpoints": {
            "GET all operators": "/operators",
            "GET operator by ID": "/operators/<id>",
            "POST new operator": "/operators (POST)",
            "PUT update operator": "/operators/<id> (PUT)",
            "DELETE operator": "/operators/<id> (DELETE)",
            "SEARCH operators": "/operators/search?name=&class=&subclass="
        }
    }

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin123":
        token = create_access_token(identity=username)
        return {"access_token": token}, 200

    return {"error": "Invalid credentials"}, 401

@app.route("/operators", methods=["GET"])
def get_operators():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM operators")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()

    data = [dict(zip(columns, row)) for row in rows]
    return format_response(data, root="operators")

@app.route("/operators/<int:id>", methods=["GET"])
def get_operator(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM operators WHERE id=%s", (id,))
    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()

    if not row:
        return {"error": "Operator not found"}, 404

    data = dict(zip(columns, row))
    return format_response(data, root="operator")

@app.route("/operators", methods=["POST"])
@jwt_required()
def add_operator():
    data = request.get_json() or {}
    required = ["operator_name", "class", "subclass"]
    missing = [f for f in required if f not in data]
    if missing:
        return {"error": f"Missing fields: {', '.join(missing)}"}, 400

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO operators (operator_name, class, subclass) VALUES (%s, %s, %s)",
            (data["operator_name"], data["class"], data["subclass"])
        )
        mysql.connection.commit()
        new_id = cursor.lastrowid
    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}, 500
    finally:
        cursor.close()

    return {"message": "Operator added", "id": new_id}, 201

@app.route("/operators/<int:id>", methods=["PUT"])
@jwt_required()
def update_operator(id):
    data = request.get_json() or {}
    fields = ["operator_name", "class", "subclass"]
    updates = {k: data[k] for k in fields if k in data}

    if not updates:
        return {"error": "No valid fields to update"}, 400

    set_clause = ", ".join(f"{k}=%s" for k in updates.keys())
    values = list(updates.values()) + [id]

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(f"UPDATE operators SET {set_clause} WHERE id=%s", values)
        mysql.connection.commit()
        if cursor.rowcount == 0:
            return {"error": "Operator not found"}, 404
    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}, 500
    finally:
        cursor.close()

    return {"message": "Operator updated"}

@app.route("/operators/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_operator(id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM operators WHERE id=%s", (id,))
        mysql.connection.commit()
        if cursor.rowcount == 0:
            return {"error": "Operator not found"}, 404
    except Exception as e:
        mysql.connection.rollback()
        return {"error": str(e)}, 500
    finally:
        cursor.close()

    return {"message": "Operator deleted"}


@app.route("/operators/search", methods=["GET"])
def search_operators():
    name = request.args.get("name")
    cls = request.args.get("class")
    subclass = request.args.get("subclass")

    query = "SELECT * FROM operators"
    filters = []
    values = []

    if name:
        filters.append("operator_name LIKE %s")
        values.append(f"%{name}%")
    if cls:
        filters.append("class LIKE %s")
        values.append(f"%{cls}%")
    if subclass:
        filters.append("subclass LIKE %s")
        values.append(f"%{subclass}%")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    cursor = mysql.connection.cursor()
    cursor.execute(query, tuple(values))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()

    data = [dict(zip(columns, row)) for row in rows]
    return format_response(data, root="operators")


if __name__ == "__main__":
    app.run(debug=True)
