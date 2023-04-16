import json

from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)

api = Api(app)
ERRORS = json.load(open("errors.json", "r"))


# type: ignore
class User(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"username={self.username} - password={self.password}"


class DBLogin(Resource):
    def get(self, user_key):
        result = User.query.get(key=user_key)
        pass


class LoginRequest(Resource):

    def validate_query(self, user_key):
        result = User.query.filter_by(key=user_key).first()
        if not result:
            abort(404, message=ERRORS["404"])
        return result

    user_fields = {
        "username": fields.String,
        "password": fields.String
    }
    # create login requirements to be parsed
    parse_login = reqparse.RequestParser()
    parse_login.add_argument("username", type=str,
                             help="username", required=True)
    parse_login.add_argument("password", type=str,
                             help="password", required=True)

    update_login = reqparse.RequestParser()
    update_login.add_argument("username", type=str,
                              help="username", required=False)
    update_login.add_argument("password", type=str,
                              help="password", required=False)

    @marshal_with(user_fields)
    def get(self, user_key):
        # query the database using the user_key
        return self.validate_query(user_key)

        # user_key = str(user_key)

        # keys = read_json_file("keys.json")
        # return keys[user_key] if user_key in keys else abort(404, ERRORS["404"])

    def post(self, user_key):
        args = self.parse_login.parse_args()

        # check if args is malformed
        if not args["username"] or not args["password"]:
            abort(400, message=ERRORS["400"])

        user = User(
            key=user_key, username=args["username"], password=args["password"])
        db.session.add(user)
        db.session.commit()

        return "account_created", 201

        # keys = read_json_file("keys.json")
        # if str(user_key) in keys:
        #     return ERRORS["400"], 400

        # args = self.parse_login.parse_args()
        # keys[user_key] = args

        # save_to_json("keys.json", keys)
        # return "account_created", 201

    def delete(self, user_key):
        result = self.validate_query(user_key)
        db.session.delete(result)
        db.session.commit()

    def patch(self, user_key):
        result = self.validate_query(user_key)
        args = self.update_login.parse_args()

        if args["username"]:
            result.username = args["username"]

        if args["password"]:
            result.password = args["password"]

        db.session.commit()

        # keys = read_json_file("keys.json")
        # if str(user_key) not in keys:
        #     return ERRORS["404"], 404

        # # return the datatype of keys
        # del keys[str(user_key)]
        # save_to_json("keys.json", keys)
        # return ERRORS["200"], 200

        # add the resource to the api
api.add_resource(LoginRequest, "/def/<int:user_key>")


def read_json_file(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # if the file doesn't exist, create it
        with open(filename, "w") as f:
            json.dump({}, f)
            return {}


def save_to_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    app.run(debug=True)
