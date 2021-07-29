from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {	'username': 'Jackson',
                 'email': 'jackson@gmail.com', }


api.add_resource(HelloWorld, "/users")


if __name__ == "__main__":
    app.run(debug=True)
