import pymongo
import jsonschema
from jsonschema import validate

MONGO_HOST = 'ds149742.mlab.com'
MONGO_PORT = 49742
MONGO_DB   = 'heroku_776l5bh4'
MONGO_USER = 'connection_user'
MONGO_PASS = 'cakiproject123'
BOOKS_COLL = 'books'
USERS_COLL = 'users'

connection = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = connection[MONGO_DB]
db.authenticate(MONGO_USER, MONGO_PASS)

books_v = {
      "$jsonSchema": {
          "bsonType": "object",
          "required": [ "name", "price"],
          "properties": {
            "name": {
               "bsonType": "string",
               "description": "unique index, string from 3 to 15 characters",
               "minLength": 3,
               "maxLength": 15
            },
            "price": {
               "bsonType": "number",
               "description": "price as number from 1 to 10000",
               "minimum": 1,
               "maximum": 10000
            },
            "description": {
               "bsonType": "string",
               "description": "string from 10 to 150 characters",
               "minLength": 10,
               "maxLength": 150
            },
            "quantity": {
               "bsonType": "number",
               "description": "number of boks as number from 1 to 10, default is 1",
            #    "default": 1,
               "minimum": 1,
               "maximum": 10
            },
            "image": {
               "bsonType": "string",
               "description": "image path as string from 5 to 150 characters",
            #    "default": "default.png",
               "minimum": 5,
               "maximum": 150
            },
            "pages": {
               "bsonType": "number",
               "description": "number of book pages from 10 to 5000",
               "minimum": 10,
               "maximum": 50000
            }
          }
      }
    }


# books_col = db.create_collection("books_test", validator=books_v)
books_col = db["books_test"]

# Svaki user je opisan sledecim atributima:
#   name - String required
#   year - Number required 

try:
    my_book_1 = { 
        "name": "Staki",
        "price": 20,
        "description": "neki glupi opis",
        "quantity": 7,
        "pages": 1245,
        "image": "staki.jpg"
    }
    doc1 = books_col.insert_one(my_book_1)
except Exception as e:
    print(e)

try:
    my_book_2 = { 
        "name": "Aki",
        "price": 2000,
        "description": "neki glupi opis",
        "quantity": 4,
        "pages": 1245,
        "image": "aki.jpg"
    }
    doc2 = books_col.insert_one(my_book_2)
except Exception as e:
    print(e)