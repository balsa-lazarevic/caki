import os
import re
from functools import wraps

from werkzeug.utils import redirect, secure_filename
from flask import Flask, request, render_template, url_for, make_response, session, jsonify, json, flash
# from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource, Api, reqparse
from bson.json_util import dumps
from config import *
# from user import authenticate, identity
from users import users_v
from books import books_v
from bson import json_util, ObjectId
import hashlib


# from logger import log

# Validator
def validate(to_validate, name):
    if name == 'book':
        # name
        if len(to_validate.name) > 15:
            print('The name is too long, max input is 15 characters')
            return False
        if len(to_validate.name) < 3:
            print('The name is too short, min input is 3 characters')
            return False

        # description
        if len(to_validate.description) > 150:
            print('The description is too long, max input is 150 characters')
            return False
        if len(to_validate.description) < 10:
            print('The description is too short, min input is 10 characters')
            return False

        # TODO image

        # price
        if type(to_validate.price) != float:
            to_validate.price = float(to_validate.price)
        if to_validate.price > 10000.00:
            print('Max price input is 10000')
            return False
        if to_validate.price < 1.00:
            print('Min price input is 1')
            return False

        # quantity
        if to_validate.quantity > 10:
            print('Max quantity input is 10')
            return False
        if to_validate.quantity < 1:
            print('Min quantity input is 1')
            return False

        # pages
        if to_validate.pages > 5000:
            print('Max pages input is 5000')
            return False
        if to_validate.pages < 10:
            print('Min pages input is 10')
            return False

    if name == 'user':
        # name
        if len(to_validate.name) > 20:
            print('The name is too long, max input is 20 characters')
            return False
        if len(to_validate.name) < 3:
            print('The name is too short, min input is 3 characters')
            return False
        # password
        if len(to_validate.password) > 25:
            print('The password is too long, max input is 25 characters')
            return False
        if len(to_validate.password) < 5:
            print('The password is too short, min input is 5 characters')
            return False
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{5,})", to_validate.password)):
            print('Password is too weak, please try with a stronger password')
            return False
        # role
        if to_validate.role > 1 or to_validate.role < 0:
            print('User role must be either user or administrator')
            return False
        # book
        if to_validate.book and type(to_validate.book) not in list:
            print('List of books not provided')
            return False

    return True


if not "users" in db.list_collection_names():
    users_coll = db.create_collection('users', validator=users_v)
    users_coll.create_index('index', unique=True)
else:
    users_coll = db['users']

if not "books" in db.list_collection_names():
    books_coll = db.create_collection('books', validator=books_v)
    books_coll.create_index('index', unique=True)
else:
    books_coll = db['books']

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()
api = Api(app)
# jwt = JWT(app, authenticate, identity)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def index():
    resp = make_response("INDEX")
    resp.set_cookie('username', 'the username')
    return resp


@app.route('/logg')
@login_required
def logg():
    return render_template("index.html")


@app.route('/home')
def home():
    # TODO if user is loged in  return render_template("index.html")
    # TODO if user is not loged in:
    return render_template("base.html")


# @app.route('/home')
# def home():
#     if 'username' in session:
#             return 'Logged in as %s' % escape(session['username'])
#     print(session)
#     return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    error = ''
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            hashed = hashlib.sha256(attempted_password.encode('ascii'))
            password = hashed.hexdigest()

            user_exists = list(users_coll.find({"username": attempted_username}))

            if user_exists[0]["role"] == 1:
                session['logged_in'] = True
                session['username'] = attempted_username
                return redirect(url_for('logg'))
            elif user_exists[0]["username"] == str(attempted_username) and user_exists[0]["password"] == str(password):
                session['logged_in'] = True
                session['username'] = attempted_username
                return redirect(url_for('logg'))
            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error=error)
    except Exception as e:
        print(e)
        return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    session.clear()
    # remove the username from the session if it's there
    # session.pop('username', None)
    return redirect(url_for('home'))


#
# @app.route('/register')
# def register():
#     return render_template("registration_form.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            hashed = hashlib.sha256(password.encode('ascii'))
            password = hashed.hexdigest()

            user_exists = list(users_coll.find({"username": username}))
            email_exists = list(users_coll.find({"email": email}))
            if user_exists:
                print("Pick another username!")
                return render_template("registration_form.html")
            elif email_exists:
                print("This email already registered!")
                return render_template("registration_form.html")
            else:
                new_user = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "role": 0
                }
                users_coll.insert_one(new_user)
                session['logged_in'] = True
                session['username'] = username
                return dumps(new_user), 201

        return render_template("registration_form.html")
    except Exception as e:
        print(e)
        return render_template("registration_form.html")


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


# @app.route('/protected')
# @jwt_required()
# def protected():
#     return '%s' % current_identity

# Ja
class User(Resource):
    def get(self, name):
        try:
            user = list(users_coll.find({"username": name}))
            if user:
                # return json.loads(json_util.dumps(user)), 200
                return dumps(user), 200
            else:
                return {"message": "User with this username not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def post(self, name):
        try:
            request_data = request.get_json()
            hash = hashlib.sha256(request_data["password"].encode('ascii'))
            new_user = {
                "username": request_data["username"],
                "email": request_data["email"],
                "password": hash.hexdigest(),
                "role": request_data["role"]
            }
            users_coll.insert_one(new_user)
            return dumps(new_user), 201
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def delete(self, name):
        try:
            user = users_coll.find_one_and_delete({"username": name})
            if user:
                return {"message": "User deleted."}, 200
            else:
                return {"message": "User with this username not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    # @jwt_required()
    def put(self, name):
        try:
            '''
            request_data = request.get_json()'''
            user = list(users_coll.find({"username": name}))
            # print(user)
            parser = reqparse.RequestParser()
            is_required = False
            if not user:
                is_required = True
            else:
                user = user[0]
            parser.add_argument("username", type=str, required=is_required)
            parser.add_argument("email", type=str, required=is_required)
            parser.add_argument("password", type=str, required=is_required)
            parser.add_argument("role", type=bool, required=is_required)
            request_data = parser.parse_args()

            new_user = {
                "username": request_data["username"] if request_data["username"] else user["username"],
                "email": request_data["email"] if request_data["email"] else user["email"],
                "password": request_data["password"] if request_data["password"] else user["password"],
                "role": request_data["role"] if request_data["role"] else user["role"],
            }

            if not user:
                users_coll.insert_one(new_user)
                return dumps(new_user), 201
            else:
                users_coll.update_one({"username": name}, {"$set": new_user})
                return {"message": "Updated"}, 200

        except Exception as e:
            return {"error": str(e)}, 400


@app.route("/users")
def users():
    try:
        books = []
        users = list(users_coll.find())
        for i in json.loads(json_util.dumps(users)):
            b = list(books_coll.find({"user_id": ObjectId(i["_id"]["$oid"])}))
            if len(b) > 0:
                books.append(b)
        # print(books)
        if users:
            return render_template('test.html', e_list=json.loads(json_util.dumps(users)))
        else:
            return {"message": "No users found."}, 404
    except Exception as e:
        return dumps({"error": str(e)})


api.add_resource(User, "/user/<string:name>")


class Books(Resource):
    def get(self, name):
        try:
            book = list(books_coll.find({"name": name}))
            if book:
                data = json.loads(json_util.dumps(book))
                return dumps(book), 200
            else:
                return {"message": "Book with this name not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400


@app.route("/books")
def books():
    try:
        books = list(books_coll.find())
        print(json.loads(json_util.dumps(books)))
        if books:
            return render_template('test.html', e_list=json.loads(json_util.dumps(books)))
        else:
            return None, 404
    except Exception as e:
        return dumps({"error": str(e)})


# api.add_resource(Books, "/book/<string:name>")
# api.add_resource(BooksList, "/books")

app.run(port=5000, debug=True)
