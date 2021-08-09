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



def abort_if_user_doesnt_exist(user_id):
    if user_id not in users:
        abort(404, message ="User id is not valid")

def abort_if_user_exists(user_id):
    if user in users:
        abort(409, message="User already exists with that id")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MiAccount3' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' ##location of our database
api = Api(app)
db = SQLAlchemy(app)



## The Database Models
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Integer, nullable=False)

class AccountModel(db.Model): 
    accountId = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, foreign_key=True) #maps to the user of the acccount
    accountType = db.Column(db.String, nullable=False)
    accountNumber = db.Column(db.String, nullable=False)
    accountBalance = db.Column(db.Integer, nullable=False)



# db.create_all() # Already Created !


## The Routes
@app.route('/signup', methods=['POST'])
def signUp():
    abort(abort_if_user_exists)
    args = users_put_args.parse_args()
    return "Welcome to MiAccount", 201

@app.route('/login', methods=['POST'])
def login():
    abort_if_user_doesnt_exist(user_id)
    if name in args:
        return 'Successfull login', 200        
    return make_response("Couldn't verify!", 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/delete', methods=['DELETE'])
def deleteAccount():
    abort_if_user_doesnt_exist(user_id)
    del users[user_id]
    return 'User Deleted Successfully', 204



@app.route('/deposit', methods=['POST'])
def deposit():
    return "Deposit Successful", 200


@app.route('/checkbalance', methods=['POST'])
def checkbalance():
    result = AccountModel.query.get(balance)
    return {users[name], accounts[account], accounts[balance]}, 200

@app.route('/transfer', methods=['POST'])
def transfer():
    return {message, paymentId}, 200



if __name__ == "__main__":
    app.run(debug=True)
