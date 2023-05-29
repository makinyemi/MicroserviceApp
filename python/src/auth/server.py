import jwt, datetime, os
from flask import Flask, request 
from flask_mysqldb import MySQL

app = Flask(__name__) 
mysql = MySQL(app) 

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST") 
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# Login User
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

#Validate JWT token
@app.route("/validate", methods=["POST"])
def validate():
    token = request.headers["Authorization"]
    if not token:
        return "Missing credentials", 401
    
    token = token.split(" ")[1]

    try:
        data = jwt.decode(token, app.config["SECRET_KEY"], algorithm="HS256")
    except:
        return "Not authorized", 403

    return data ,200


#Create JWT token
def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
            "secret": secret,
        },
        secret,
        algorithm="HS256"
    )


if __name__ == "__main__": #runs our app
    app.run(host="0.0.0.0", port=5000) #tells flask app to listen on all public IPs on host network and port 5000