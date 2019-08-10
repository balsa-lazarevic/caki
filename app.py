import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from bson.json_util import dumps
from config import *

app = Flask(__name__)
api = Api(app)


@app.route('/')
# @app.route('/index')
def home():
    #if user is loged in
    # return render_template("index.html")
    #if user is not loged in
    return render_template("base.html")

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("registration_form.html")

if __name__ == "__main__":
    app.run(debug=True)
app.run(port=5000)


class Book(Resource):

    def get(self, name):
        try:
            book = list(books_col.find({"name": name}))
            if len(book) > 0:
                return dumps(book), 200
            else:
                return None, 404
        except Exception as e:
            return {"error": str(e)}, 400

    def post(self, name):
        try:
            request_data = request.get_json()
            upload_image = request.files['image']
            upload_image.save(os.path.join(app.instance_path, 'uploads', secure_filename(upload_image.filename)))
            upload_image_url = '127.0.0.1:5000/uploads/' + upload_image.filename

            new_book = {
                "name": request_data["name"],
                "description": request_data["description"],
                "image": upload_image_url,
                "price": request_data["price"],
                "quantity": request_data["quantity"],
                # ToDo - get user
                "user": request_data["user"],
                "pages": request_data["pages"],
            }
            books_col.insert_one(new_book)
            return dumps(new_book), 201
        except Exception as e:
            return {"error": str(e)}, 400

    def put(self, name):
        try:
            request_data = request.get_json()
            new_book = {"$set": {
                "name": request_data["name"],
                "description": request_data["description"],
                # ToDo - upload image
                "image": request_data["image"],
                "price": request_data["price"],
                "quantity": request_data["quantity"],
                # ToDo - get user
                "user": request_data["user"],
                "pages": request_data["pages"],
            }}

            update_query = {{"name": name}}
            books_col.update_one(update_query, new_book)

            return dumps(new_book), 201
        except Exception as e:
            return {"error": str(e)}, 400

    def delete(self, name):
        try:
            student = books_col.find_one_and_delete({"name": name})
            if student:
                return {"message": "Book deleted."}, 200
                # return dumps(new_book), 201
            else:
                return {"message": "Book with this name not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400


class Books(Resource):

    def get(self):
        try:
            request_data = request.get_json()
            books = list(books_col.find())
            if books:
                return dumps(books), 200
            else:
                return None, 404
        except Exception as e:
            return dumps({"error": str(e)})


class User(Resource):

    def get(self, name):
        try:
            request_data = request.get_json()
            user = list(users_col.find({"name": name}))
            if len(user) > 0:
                return dumps(user), 200
            else:
                return None, 404
        except Exception as e:
            return {"error": str(e)}, 400

    def post(self, name):
        try:
            request_data = request.get_json()
            new_user = {
                "name": request_data["name"],
                "description": request_data["description"],
                "image": request_data["image"],
                "price": request_data["price"],
                "quantity": request_data["quantity"],
                "user": request_data["user"],
                "pages": request_data["pages"],
            }
            users_col.insert_one(new_user)
            return dumps(new_user), 201
        except Exception as e:
            return {"error": str(e)}, 400

    def put(self, name):
        try:
            request_data = request.get_json()
            new_user = {"$set": {
                "name": request_data["name"],
                "description": request_data["description"],
                "image": request_data["image"],
                "price": request_data["price"],
                "quantity": request_data["quantity"],
                "user": request_data["user"],
                "pages": request_data["pages"],
            }}

            update_query = {{"name": name}}
            users_col.update_one(update_query, new_user)

            return dumps(new_user), 201
        except Exception as e:
            return {"error": str(e)}, 400

    def delete(self, name):
        try:
            student = users_col.find_one_and_delete({"name": name})
            if student:
                return {"message": "User deleted."}, 200
            else:
                return {"message": "User with this name not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400


class Users(Resource):

    def get(self):
        try:
            users = list(users_col.find())
            if users:
                return dumps(users), 200
            else:
                return None, 404
        except Exception as e:
            return dumps({"error": str(e)})


api.add_resource(User, "/book/<string:name>")
api.add_resource(Users, "/books")

api.add_resource(User, "/user/<string:name>")
api.add_resource(Users, "/users")

app.run(port=5000, debug=True)
