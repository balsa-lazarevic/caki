import config
import books
import users

print(MONGO_HOST)
connection = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = connection[MONGO_DB]
db.authenticate(MONGO_USER, MONGO_PASS)

# books
if "books" in db.list_collection_names():
    books_col = db["books"]
    books_col.create_index("name", unique=True)
else:
    books_col = db.create_collection("books", validator=books_v)

# users
if "users" in db.list_collection_names():
    users_col = db["users"]
    users_col.create_index("username", unique=True)
else:
    users_col = db.create_collection("users", validator=users_v)

# users testing
try:
    users_col.insert_one({
        "username": "Aki",
        "password": "d7d05512c864a5f867eff324ee146a3ad4fb0e4fe8c7cb679dfb3ee95592a2ea",
        "email": "aki@gmail.com",
        "role": 1
        }
    )
except Exception as e:
    print(e)

try:
    users_col.insert_one({
        "username": "Staki2",
        "password": "d7d05512c864a5f867eff324ee146a3ad4fb0e4fe8c7cb679dfb3ee95592a2ea",
        "email": "aki@gmail.com",
        "role": 0
        }
    )
except Exception as e:
    print(e)

user_sel = users_col.find_one()
# print(user_sel["_id"])
# print(type(user_sel["_id"]))
# books testing
try:
    books_col.insert_one({
        "user_id": user_sel,
        "name": "Staki",
        "price": 20.34,
        "description": "neki glupi opis",
        "quantity": 7,
        "pages": 1245,
        "image": "staki.jpg"
        }
    )
except Exception as e:
    print(e)

try:
    books_col.insert_one({
        "user_id": user_sel,
        "name": "Aki",
        "price": 2000,
        "description": "neki glupi opis",
        "quantity": 4,
        "pages": 1245,
        "image": "aki.jpg"
    }
    )
except Exception as e:
    print(e)

connection.close()
