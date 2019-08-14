import os
import re
import hashlib
from werkzeug.utils import redirect
from flask import Flask, request, render_template, url_for, make_response, session
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse
from bson.json_util import dumps
from config import *
from security import authenticate, identity
from users import users_v
from books import books_v

# from logger import log

# Validator


def validate(toValidate, name):
    if name == 'book':
        # name
        if(len(toValidate.name) > 15):
            print('The name is too long, max input is 15 characters')
            return False
        if(len(toValidate.name) < 3):
            print('The name is too short, min input is 3 characters')
            return False

        # description
        if(len(toValidate.description) > 150):
            print('The description is too long, max input is 150 characters')
            return False
        if(len(toValidate.description) < 10):
            print('The description is too short, min input is 10 characters')
            return False

        # TODO image

        # price
        if(toValidate.price > 10000):
            print('Max price input is 10000')
            return False
        if(toValidate.price < 1):
            print('Min price input is 1')
            return False

        # quantity
        if(toValidate.quantity > 10):
            print('Max quantity input is 10')
            return False
        if(toValidate.quantity < 1):
            print('Min quantity input is 1')
            return False

        # pages
        if(toValidate.pages > 5000):
            print('Max pages input is 5000')
            return False
        if(toValidate.pages < 10):
            print('Min pages input is 10')
            return False

    elif name == 'user':
        # name
        if(len(toValidate.name) > 20):
            print('The name is too long, max input is 20 characters')
            return False
        if(len(toValidate.name) < 3):
            print('The name is too short, min input is 3 characters')
            return False
        # password
        if(len(toValidate.password) > 25):
            print('The password is too long, max input is 25 characters')
            return False
        if(len(toValidate.password) < 5):
            print('The password is too short, min input is 5 characters')
            return False
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{5,})", toValidate.password)):
            print('Password is too weak, please try with a stronger password')
            return False
        # role
        if(toValidate.role > 1 or toValidate.role < 0):
            print('User role must be either user or administrator')
            return False
        # book
        if(toValidate.book and type(toValidate.book) not list):
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
jwt = JWT(app, authenticate, identity)


@app.route('/')
def index():
    resp = make_response("INDEX")
    resp.set_cookie('username', 'the username')
    return resp


@app.route('/logg')
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
#     return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     session['username'] = request.form['username']
    #     return redirect(url_for('home'))
    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/register')
def register():
    return render_template("registration_form.html")


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


class User(Resource):
    def get(self, name):
        try:
            user = list(users_coll.find({"username": name}))
            if user:
                return dumps(user), 200
            else:
                return {"message": "User with this username not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def post(self, name):
        try:
            request_data = request.get_json()
            new_user = {
                "username": request_data["name"],
                "email": request_data["email"],
                "password": request_data["password"],
                "role": request_data["role"],
                "book": request_data["book"],
            }

            validated = validate(new_user, 'user')

            if not validated:
                return {"error": "validation failed"}, 400

            # hash password
            hash_orig = hashlib.sha256(new_user.password.encode('utf-8'))
            hash_pass = hash_orig.hexdigest()
            new_user.password = hash_pass

            users_coll.insert_one(new_user)
            return dumps(new_user), 201
        except Exception as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def delete(self, name):
        try:
            user = users_coll.find_one_and_delete({"username": name})
            if user:
                return {"message": "User deleted."}, 200
            else:
                return {"message": "User with this username not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def put(self, name):
        try:
            '''
            request_data = request.get_json()'''
            user = list(users_coll.find({"username": name}))
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
            parser.add_argument("book")
            request_data = parser.parse_args()

            new_user = {
                "username": request_data["username"] if request_data["username"] else user["username"],
                "email": request_data["email"] if request_data["email"] else user["email"],
                "password": request_data["password"] if request_data["password"] else user["password"],
                "role": request_data["role"] if request_data["role"] else user["role"],
                "book": request_data["book"] if request_data["book"] else user["book"],
            }

            validated = validate(new_user, 'user')

            if not validated:
                return {"error": "validation failed"}, 400

            if not user:
                users_coll.insert_one(new_user)
                return dumps(new_user), 201
            else:
                users_coll.update_one({"username": name}, {"$set": new_user})
                return {"message": "Updated"}, 200

        except Exception as e:
            return {"error": str(e)}, 400


class UserList(Resource):
    def get(self):
        # return 1
        try:
            users = list(users_coll.find())
            if users:
                return dumps(users), 200
            else:
                return {"message": "No users found."}, 404
        except Exception as e:
            return dumps({"error": str(e)})


api.add_resource(User, "/user/<string:name>")
api.add_resource(UserList, "/users")


class Books(Resource):
    def get(self, name):
        try:
            book = list(books_coll.find({"name": name}))
            if book:
                return dumps(book), 200
            else:
                return {"message": "Book with this name not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def post(self, name):
        try:
            request_data = request.get_json()
            new_book = {
                "name": request_data["name"],
                "description": request_data["description"],
                "image": request_data["image"],
                "price": request_data["price"],
                "quantity": request_data["quantity"],
                "user": request_data["user"],
                "pages": request_data["pages"],
            }

            # check book quantity - default value
            if not new_book.quantity:
                new_book.quantity = 1

            validated = validate(new_book, 'book')

            if not validated:
                return {"error": "validation failed"}, 400

            books_coll.insert_one(new_book)
            return dumps(new_book), 201
        except Exception as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def delete(self, name):
        try:
            book = books_coll.find_one_and_delete({"name": name})
            if book:
                return {"message": "Book deleted."}, 200
            else:
                return {"message": "Book with this name not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def put(self, name):
        try:
            '''
            request_data = request.get_json()'''
            book = list(books_coll.find({"name": name}))
            parser = reqparse.RequestParser()
            is_required = False
            if not book:
                is_required = True
            else:
                book = book[0]
            parser.add_argument("name", type=str, required=is_required)
            parser.add_argument("description", type=str, required=is_required)
            parser.add_argument("image", type=str, required=is_required)
            parser.add_argument("price", type=bool, required=is_required)
            parser.add_argument("quantity", type=bool, required=is_required)
            parser.add_argument("user", type=bool, required=is_required)
            parser.add_argument("pages", type=bool, required=is_required)
            request_data = parser.parse_args()

            new_book = {
                "name": request_data["name"] if request_data["name"] else book["name"],
                "description": request_data["description"] if request_data["description"] else book["description"],
                "image": request_data["image"] if request_data["image"] else book["image"],
                "price": request_data["price"] if request_data["price"] else book["price"],
                "quantity": request_data["quantity"] if request_data["quantity"] else book["quantity"],
                "user": request_data["user"] if request_data["user"] else book["user"],
                "pages": request_data["pages"] if request_data["pages"] else book["pages"],
            }

            validated = validate(new_book, 'book')

            if not validated:
                return {"error": "validation failed"}, 400

            if not book:
                books_coll.insert_one(new_book)
                return dumps(new_book), 201
            else:
                books_coll.update_one({"name": name}, {"$set": new_book})
                return {"message": "Updated"}, 200

        except Exception as e:
            return {"error": str(e)}, 400


class BooksList(Resource):
    def get(self):
        try:
            books = list(books_coll.find())
            if books:
                return dumps(books), 200
            else:
                return None, 404
        except Exception as e:
            return dumps({"error": str(e)})


api.add_resource(Books, "/book/<string:name>")
api.add_resource(BooksList, "/books")

app.run(port=5000, debug=True)
# ToDo VALIDATORI ZA BAZU PREKO PYTHONA
