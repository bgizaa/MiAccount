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



app = Flask(__name__)
app.config['SECRET_KEY'] = 'MiAccount3' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' ##location of our database
api = Api(app)
db = SQLAlchemy(app)
# db.create_all() # Run once !



## The Database Models

class AccountUserModel(db.Model):
	name = db.Column(db.String(100), nullable=False, primary_key=True)
	email = db.Column(db.Integer, nullable=False)
	password = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"name = {name}, email = {email},password = {password})"

class AccountsModel(db.Model):
	# id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.String(100), nullable=False, primary_key=True)
	amount = db.Column(db.Integer, nullable=False)
	currency = db.Column(db.String, nullable=False)
	accountType = db.Column(db.String, nullable=False)


	def __repr__(self):
		return f"name = {name}, amount = {amount}, currency = {currency}, accountType = {accountType})"


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("email", type=str, help="Email of the user", required=True)
user_put_args.add_argument("password", type=str, help="Password of the user", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("email", type=str, help="Email of the user")
user_update_args.add_argument("password", type=str, help="Password of the user")


accounts_put_args = reqparse.RequestParser()
accounts_put_args.add_argument("number",type=str,help="Number is required", required=True)
accounts_put_args.add_argument("amount",type=int,help="Amount is required", required=True)
accounts_put_args.add_argument("currency",type=str,help="Currency is required", required=True)
accounts_put_args.add_argument("accountType",type=str,help="Type is required", required=True)


accounts_update_args = reqparse.RequestParser()
accounts_update_args.add_argument("number",type=str,help="Number is required", required=True)
accounts_update_args.add_argument("amount",type=int,help="Amount is required", required=True)
accounts_update_args.add_argument("currency",type=str,help="Currency is required", required=True)
accounts_update_args.add_argument("accountType",type=str,help="accountType is required", required=True)

resource_fields = {
    'email': fields.String,
	'password': fields.String
}


account_resource_fields = {
      'number': fields.String,
	  'amount': fields.Integer,
	  'currency': fields.String,
	  'accountType': fields.String
}


class User(Resource):
	@marshal_with(resource_fields)
	def get(self, name):
		result = AccountUserModel.query.filter_by(name=name).first()
		if not result:
			abort(404, message="Could not find user with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, name):
		args = user_put_args.parse_args()
		result = AccountUserModel.query.filter_by(name=name).first()
		if result:
			abort(409, message="User id taken...")

		user = AccountUserModel(name=name, email=args['email'], password=args['password'])
		db.session.add(user)
		db.session.commit()
		return user, 201

	@marshal_with(resource_fields)
	def patch(self, name):
		args = user_update_args.parse_args()
		result = AccountUserModel.query.filter_by(name=name).first()
		if not result:
			abort(404, message="User doesn't exist, cannot update")

	
		if args['email']:
			result.email = args['email']
		if args['password']:
			result.password = args['password']

		db.session.commit()

		return result


class Account(Resource):
	@marshal_with(account_resource_fields)
	def get(self, number):
		result = AccountsModel.query.filter_by(number=number).first()
		if not result:
			abort(404, message="Could not find Account number")
		return result


	@marshal_with(account_resource_fields)
	def put(self, number):
		args = accounts_put_args.parse_args()
		result = AccountsModel.query.filter_by(number=number).first()
		if result:
			abort(409, message="Account number taken...")

		account = AccountsModel(number=number, amount=args['amount'], currency=args['currency'], accountType=args['accountType'])
		db.session.add(account)
		db.session.commit()
		return account, 201

api.add_resource(User, "/user/<string:name>")
api.add_resource(Account, "/account/<string:number>")



# def init_db():
#     db.create_all()
	

if __name__ == "__main__":
    # init_db()
    app.run(debug=True)
