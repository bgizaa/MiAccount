from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import jwt
import datetime
from functools import wraps



users_put_args = reqparse.RequestParser()
users_put_args.add_argument("name",type=str,help="Name is required", required=True)
users_put_args.add_argument("email",type=str,help="Email is required", required=True)



users = {}


accounts = {}



def abort_if_user_id_doesnt_exist(user_id):
    if user_id not in users:
        abort("User id is not valid")



app = Flask(__name__)
app.config['SECRET_KEY'] = 'MiAccount3' 
api = Api(app)


@app.route('/signup', methods=['POST'])
def post():
    args = users_put_args.parse_args()
    return "Welcome to MiAccount", 201

@app.route('/login', methods=['POST'])
def get():
    if name in args:
        return 'Successfull login', 200
        
    return make_response("Couldn't verify!", 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


@app.route('/deposit', methods=['POST'])
def post():
    return "Deposit Successful", 200


@app.route('/checkbalance', methods=['POST'])
def post():
    return {users[name], accounts[account], accounts[balance]}, 200

@app.route('/tranfer', methods=['POST'])
def post():
    return {message, paymentId}, 200



if __name__ == "__main__":
    app.run(debug=True)
