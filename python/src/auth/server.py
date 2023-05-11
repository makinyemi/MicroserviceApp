from flask import Flask, request 
from flask_mysqldb import MySQL 


app = Flask(__name__) 
mysql = MySQL(app) 

