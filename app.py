import gc
import os
import re
from functools import wraps
from werkzeug.utils import redirect, secure_filename
from flask import Flask, request, render_template, url_for, make_response, session, json, flash
from flask_restful import Resource, Api, reqparse
from bson.json_util import dumps
from config import *
from users import users_v
from books import books_v
from bson import json_util, ObjectId
import hashlib
# from logger import log


def validate(to_validate, name):
    if name == 'book':
        # name
        if len(to_validate.name) > 15:
            flash('The name is too long, max input is 15 characters', category='error')
            return False
        if len(to_validate.name) < 3:
            flash('The name is too short, min input is 3 characters', category='error')
            return False

        # description
        if len(to_validate.description) > 150:
            flash('The description is too long, max input is 150 characters', category='error')
            return False
        if len(to_validate.description) < 10:
            flash('The description is too short, min input is 10 characters', category='error')
            return False

        # TODO image

        # price
        if type(to_validate.price) != float:
            to_validate.price = float(to_validate.price)
        if to_validate.price > 10000.00:
            flash('Max price input is 10000', category='error')
            return False
        if to_validate.price < 1.00:
            flash('Min price input is 1', category='error')
            return False

        # quantity
        if to_validate.quantity > 10:
            flash('Max quantity input is 10', category='error')
            return False
        if to_validate.quantity < 1:
            flash('Min quantity input is 1', category='error')
            return False

        # pages
        if to_validate.pages > 5000:
            flash('Max pages input is 5000', category='error')
            return False
        if to_validate.pages < 10:
            flash('Min pages input is 10', category='error')
            return False

    if name == 'user':
        # name
        if len(to_validate.name) > 20:
            flash('The name is too long, max input is 20 characters', category='error')
            return False
        if len(to_validate.name) < 3:
            flash('The name is too short, min input is 3 characters', category='error')
            return False
        # password
        if len(to_validate.password) > 25:
            flash('The password is too long, max input is 25 characters', category='error')
            return False
        if len(to_validate.password) < 5:
            flash('The password is too short, min input is 5 characters', category='error')
            return False
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{5,})", to_validate.password)):
            flash('Password is too weak, please try with a stronger password', category='error')
            return False
        # role
        if to_validate.role > 1 or to_validate.role < 0:
            flash('User role must be either user or administrator', category='error')
            return False
        # book
        if to_validate.book and type(to_validate.book) not in list:
            flash('List of books not provided', category='error')
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


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!", category='error')
            return redirect(url_for('login'))

    return wrap


@app.route('/')
@login_required
def index():
    # resp = make_response("INDEX")
    # resp.set_cookie('username', 'the username')
    return render_template("show.html")


UPLOAD_FOLDER = 'C:\\Users\\pc\\Desktop\\caki\\static\\media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    error = ''
    try:
        if request.method == "POST":
            if request.files:
                image = request.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(os.path.join(UPLOAD_FOLDER, filename)))
                print("Image saved")
                # print(str(os.path.join(os.path.join(UPLOAD_FOLDER, filename))))

            user_exists = list(users_coll.find({"username": str(session["username"])}))

            # print(session["username"])
            # print(user_exists[0]["_id"])
            if request.form["quantity"] == "":
                request.form["quantity"] = "1"
            if re.match(r"([\\s])", str(request.form["name"])):
                request.form["name"] = request.form["name"].replace(" ", "+")
            print(request.form["name"])
            new_book = {
                "user_id": ObjectId(str(user_exists[0]["_id"])),
                "name": request.form["name"],
                "price": float(request.form["price"]),
                "description": request.form["description"],
                "quantity": int(request.form["quantity"]),
                "pages": int(request.form["pages"]),
                "image": str(os.path.join(os.path.join(UPLOAD_FOLDER, filename))).replace("C:\\Users\\pc\\Desktop\\caki\\", "")
            }
            print(request)

            books_coll.insert_one(new_book)
            return redirect(url_for('my_books'))
        else:
            error = "Invalid. Try Again."
            return render_template("book_form.html", error=error)
    except Exception as e:
        flash(e)
        return render_template("book_form.html", error=error)


@app.route('/logg')
@login_required
def logg():
    # print(session)
    return render_template("index.html")


@app.route('/home')
# @login_required
def home():
    # TODO if user is loged in  return render_template("index.html")
    # TODO if user is not loged in:
    return render_template("base.html")


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
            if user_exists[0]["username"] == str(attempted_username) and user_exists[0]["password"] == str(password) and user_exists[0]["role"] == 0:
                session['logged_in'] = True
                session['username'] = attempted_username
                session['role'] = 0
                return redirect(url_for('my_books'))
            elif user_exists[0]["username"] == str(attempted_username) and user_exists[0]["password"] == str(password) and user_exists[0]["role"] == 1:
                session['logged_in'] = True
                session['username'] = attempted_username
                session['role'] = 1
                flash(attempted_username, attempted_password)
                return redirect(url_for('books'))
            else:
                error = "Invalid credentials. Try Again."

        return render_template("login.html", error=error)

    except Exception as e:
        # flash(e)
        return render_template("login.html", error=error)


@app.route('/logout')
# @login_required
def logout():
    session.clear()
    [session.pop(key) for key in list(session.keys())]
    # print(session)
    flash("You have been logged out!")
    gc.collect()
    # remove the username from the session if it's there
    return redirect(url_for('home'))


@app.route("/my_books", methods=["GET", "POST"])
@login_required
def my_books():
    if request.method == "GET":
        user_exists = list(users_coll.find({"username": str(session["username"])}))
        b = list(books_coll.find({"user_id": ObjectId(str(user_exists[0]["_id"]))}))
        # print(b)
        if len(b) != 0:
            # session['logged_in'] = True
            # session['username'] = session["username"]
            return render_template('show.html', e_list=json.loads(json_util.dumps(b)))
        else:
            # session['logged_in'] = True
            return render_template('index.html')


@app.route("/my_profile", methods=["GET", "POST"])
@login_required
def my_profile():
    if request.method == "GET":
        user_exists = list(users_coll.find({"username": str(session["username"])}))
        return render_template('profile.html', user_list=json.loads(json_util.dumps(user_exists)))
    else:
        # session['logged_in'] = True
        return render_template('index.html')


@app.route("/details_<string:book_name>")
@login_required
def details(book_name):
        try:
            user_exists = list(users_coll.find({"username": str(session["username"])}))
            b = list(books_coll.find({"user_id": ObjectId(str(user_exists[0]["_id"])), "name": book_name}))
            if len(b) != 0:
                # book = json.loads(json_util.dumps(b))
                # return render_template('detail.html', book_list=json.loads(json_util.dumps(b)))
                # return str(book)
                # print(json.loads(json_util.dumps(b)))
                return render_template('detail.html', b_list=json.loads(json_util.dumps(b)))
            else:
                return render_template('show.html')
        except Exception as e:
                print(e)
                return {"error": str(e)}, 400


@app.route('/register', methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            username = request.form['username']
            email = request.form['email']
            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
                flash('Your email is not ok. Check format please!', category='error')
            password = request.form['password']
            if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{5,})", password):
                flash('Password is too weak, please try with a stronger password', category='error')
            else:
                hashed = hashlib.sha256(password.encode('ascii'))
                password = hashed.hexdigest()
                user_exists = list(users_coll.find({"username": username}))
                email_exists = list(users_coll.find({"email": email}))
                if user_exists:
                    flash("Pick another username!", category='error')
                    return render_template("registration_form.html")
                elif email_exists:
                    flash("This email already registered!", category='error')
                    return render_template("registration_form.html")
                else:
                    new_user = {
                        "username": username,
                        "email": email,
                        "password": password,
                        "role": 0
                    }
                    users_coll.insert_one(new_user)
                    user_exists = list(users_coll.find({"username": username}))
                    # print(user_exists)
                    if user_exists[0]["username"] == str(username) and user_exists[0]["password"] == str(password) and user_exists[0]["role"] == 1:
                        session['logged_in'] = True
                        session['username'] = username
                        session['role'] = 1
                        return redirect(url_for('books'))
                    else:
                        session['logged_in'] = True
                        session['username'] = username
                        session['role'] = 0
                        return redirect(url_for('my_books'))
                    # return dumps(new_user), 201

        return render_template("registration_form.html")
    except Exception as e:
        print(e)
        return render_template("registration_form.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route("/delete", methods=["GET", "DELETE", "POST"])
@login_required
def delete():
    try:
        if request.method == "POST":
            name = request.form['name']
            # print(name)
            print(request)
            book = books_coll.find_one_and_delete({"name": name})
            # print(json.loads(json_util.dumps(book, ensure_ascii=False)))
            if book:
                session['logged_in'] = True
                return render_template("show.html")
            else:
                return render_template("show.html")
    except Exception as e:
        print(e)
        return {"error": str(e)}, 400


class User(Resource):
    decorators = [login_required]

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
            # flash(user)
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
@login_required
def users():
    try:
        users = list(users_coll.find())

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
                return data, 200
            else:
                return {"message": "Book with this name not found."}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    # def post(self, name):
    #     try:
    #         request_data = request.get_json()
    #         upload_image = request.files['image']
    #         upload_image.save(os.path.join(app.instance_path, 'upload', secure_filename(upload_image.filename)))
    #         upload_image_url = '127.0.0.1:5000/upload' + upload_image.filename
    #         user_exists = list(users_coll.find({"username": str(session['username'])}))
    #         user = user_exists[0]["_id"]
    #         new_book = {
    #             "name": request_data["name"],
    #             "description": request_data["description"],
    #             "image": upload_image_url,
    #             "price": request_data["price"],
    #             "quantity": request_data["quantity"],
    #             "user": user,
    #             "pages": request_data["pages"],
    #         }
    #         books_col.insert_one(new_book)
    #         return dumps(new_book), 201
    #     except Exception as e:
    #         return {"error": str(e)}, 400

    # def put(self, name):
    #     try:
    #         request_data = request.get_json()
    #         new_book = {"$set": {
    #             "name": request_data["name"],
    #             "description": request_data["description"],
    #             "image": request_data["image"],
    #             "price": request_data["price"],
    #             "quantity": request_data["quantity"],
    #             "user": request_data["user"],
    #             "pages": request_data["pages"],
    #         }}
    #
    #         update_query = {{"name": name}}
    #         books_col.update_one(update_query, new_book)
    #
    #         return dumps(new_book), 201
    #     except Exception as e:
    #         return {"error": str(e)}, 400

    # def delete(self, name):
    #     try:
    #         student = books_col.find_one_and_delete({"name": name})
    #         if student:
    #             return {"message": "Book deleted."}, 200
    #             # return dumps(new_book), 201
    #         else:
    #             return {"message": "Book with this name not found."}, 404
    #     except Exception as e:
    #         return {"error": str(e)}, 400


@app.route("/books")
@login_required
def books():
    try:
        books = list(books_coll.find())
        #if user not admin
        if session["role"] == 0:
            print(session["role"])
            if books:
                return render_template('not_admin.html')
            else:
                return None, 404
        elif session["role"] == 1:
            if books:
                return render_template('test.html', e_list=json.loads(json_util.dumps(books)))
            else:
                return None, 404
        else:
                return None, 404
    except Exception as e:
        return dumps({"error": str(e)})

# api.add_resource(Books, "/book/<string:name>")


app.run(port=5000, debug=True)
