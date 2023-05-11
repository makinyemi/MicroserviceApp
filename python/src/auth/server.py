from flask import Flask, request 
from flask_mysqldb import MySQL 


app = Flask(__name__) 
mysql = MySQL(app) 

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Authentication details not found", 401

    cur = mysql.connection.cursor()
    res = cur.execute("SELECT email, password FROM users WHERE email = %s", [auth.username])
    cur.close()

    if res > 0:
        user = cur.fetchone()
        email = user["email"]
        password = user["password"]

        if auth.username == email and auth.password == password:
            return createJWT(email,app.config["SECRET_KEY"],True)
        else:
            return "Invalid credentials", 401
    else:
        return "User not found", 401