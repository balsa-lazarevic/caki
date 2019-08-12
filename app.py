import os
from werkzeug.utils import escape, redirect
from flask import Flask, request, render_template, url_for, make_response, session
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse
from bson.json_util import dumps
from config import *
from security import authenticate, identity
from users import users_v
from logger import log


if not "users" in db.list_collection_names():
    users_coll = db.create_collection('users', validator=users_v)
    users_coll.create_index('index', unique=True)
else:
    users_coll = db['users']


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
    #TODO if user is loged in  return render_template("index.html")
    #TODO if user is not loged in:
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


#Balsa
# class Book(Resource):
#
#     def get(self, name):
#         try:
#             book = list(books_col.find({"name": name}))
#             if len(book) > 0:
#                 return dumps(book), 200
#             else:
#                 return None, 404
#         except Exception as e:
#             return {"error": str(e)}, 400
#
#     def post(self, name):
#         try:
#             request_data = request.get_json()
#             upload_image = request.files['image']
#             upload_image.save(os.path.join(app.instance_path, 'uploads', secure_filename(upload_image.filename)))
#             upload_image_url = '127.0.0.1:5000/uploads/' + upload_image.filename
#
#             new_book = {
#                 "name": request_data["name"],
#                 "description": request_data["description"],
#                 "image": upload_image_url,
#                 "price": request_data["price"],
#                 "quantity": request_data["quantity"],
#                 # ToDo - get user
#                 "user": request_data["user"],
#                 "pages": request_data["pages"],
#             }
#             books_col.insert_one(new_book)
#             return dumps(new_book), 201
#         except Exception as e:
#             return {"error": str(e)}, 400
#
#     def put(self, name):
#         try:
#             request_data = request.get_json()
#             new_book = {"$set": {
#                 "name": request_data["name"],
#                 "description": request_data["description"],
#                 # ToDo - upload image
#                 "image": request_data["image"],
#                 "price": request_data["price"],
#                 "quantity": request_data["quantity"],
#                 # ToDo - get user
#                 "user": request_data["user"],
#                 "pages": request_data["pages"],
#             }}
#
#             update_query = {{"name": name}}
#             books_col.update_one(update_query, new_book)
#
#             return dumps(new_book), 201
#         except Exception as e:
#             return {"error": str(e)}, 400
#
#     def delete(self, name):
#         try:
#             student = books_col.find_one_and_delete({"name": name})
#             if student:
#                 return {"message": "Book deleted."}, 200
#                 # return dumps(new_book), 201
#             else:
#                 return {"message": "Book with this name not found."}, 404
#         except Exception as e:
#             return {"error": str(e)}, 400
#
#
# class Books(Resource):
#
#     def get(self):
#         try:
#             request_data = request.get_json()
#             books = list(books_col.find())
#             if books:
#                 return dumps(books), 200
#             else:
#                 return None, 404
#         except Exception as e:
#             return dumps({"error": str(e)})
#
#
# class User(Resource):
#
#     def get(self, name):
#         try:
#             request_data = request.get_json()
#             user = list(users_col.find({"name": name}))
#             if len(user) > 0:
#                 return dumps(user), 200
#             else:
#                 return None, 404
#         except Exception as e:
#             return {"error": str(e)}, 400
#
# class User(Resource):
#
#     def get(self, name):
#         try:
#             user = list(users_col.find({"name": name}))
#             if user:
#                 return dumps(user), 200
#             else:
#                 return None, 404
#         except Exception as e:
#             return {"error": str(e)}, 400
#
#     @jwt_required
#     def post(self, name):
#         try:
#             request_data = request.get_json()
#             new_user = {
#                 "name": request_data["name"],
#                 "description": request_data["description"],
#                 "image": request_data["image"],
#                 "price": request_data["price"],
#                 "quantity": request_data["quantity"],
#                 "user": request_data["user"],
#                 "pages": request_data["pages"],
#             }
#             users_col.insert_one(new_user)
#             return dumps(new_user), 201
#         except Exception as e:
#             return {"error": str(e)}, 400
#
#     @jwt_required
#     def put(self, name):
#         try:
#             request_data = request.get_json()
#             new_user = {"$set": {
#                 "username": request_data["username"],
#                 "description": request_data["description"],
#                 "image": request_data["image"],
#                 "price": request_data["price"],
#                 "quantity": request_data["quantity"],
#                 "user": request_data["user"],
#                 "pages": request_data["pages"],
#             }}
#
#             update_query = {{"username": name}}
#             users_col.update_one(update_query, new_user)
#
#             return dumps(new_user), 201
#         except Exception as e:
#             return {"error": str(e)}, 400
#
#     def delete(self, name):
#         try:
#             student = users_col.find_one_and_delete({"username": name})
#             if student:
#                 return {"message": "User deleted."}, 200
#             else:
#                 return {"message": "User with this username not found."}, 404
#         except Exception as e:
#             return {"error": str(e)}, 400
#
#
# class Users(Resource):
#
#     def get(self):
#         try:
#             users = list(users_col.find())
#             if users:
#                 return dumps(users), 200
#             else:
#                 return None, 404
#         except Exception as e:
#             return dumps({"error": str(e)})
#
#
# api.add_resource(User, "/book/<string:name>")
# api.add_resource(Users, "/books")
#
# api.add_resource(User, "/user/<string:username>")
# api.add_resource(Users, "/users")


#Ja

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

    # @jwt_required()
    def post(self, name):
        try:
            request_data = request.get_json()
            new_user = {
                "username": request_data["name"],
                "email": request_data["email"],
                "password": request_data["password"],
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
                "username": request_data["username"] if request_data["username"] else user["username"] ,
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


class UserList(Resource):
    def get(self):
        # return 1
        try:
            users = list(users_coll.find())
            print(users)
            if users:
                return dumps(users), 200
            else:
                return {"message": "No users found."}, 404
        except Exception as e:
            return dumps({"error": str(e)})


# log.info()
api.add_resource(User, "/user/<string:name>")
api.add_resource(UserList, "/users")


app.run(port=5000, debug=True)
# ToDo VALIDATORI ZA BAZU PREKO PYTHONA
