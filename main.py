import json

from flask import Flask, abort
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

ERRORS = json.load(open("errors.json", "r"))


class LoginRequest(Resource):
    # create login requirements to be parsed
    parse_login = reqparse.RequestParser()
    parse_login.add_argument("username", type=str, help="username", required=True)
    parse_login.add_argument("password", type=str, help="password", required=True)

    def get(self, user_key):
        user_key = str(user_key)

        keys = read_json_file("keys.json")
        return keys[user_key] if user_key in keys else abort(404, ERRORS["404"])

    def post(self, user_key):
        keys = read_json_file("keys.json")
        if str(user_key) in keys:
            return ERRORS["400"], 400

        args = self.parse_login.parse_args()
        keys[user_key] = args

        save_to_json("keys.json", keys)
        return "account_created", 201

    def delete(self, user_key):
        keys = read_json_file("keys.json")
        if str(user_key) not in keys:
            return ERRORS["404"], 404

        # return the datatype of keys
        del keys[str(user_key)]
        save_to_json("keys.json", keys)
        return ERRORS["200"], 200


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
