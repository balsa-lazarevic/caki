import datetime
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
          "required": [ "name", "price" ],
          "properties": {
            # "user_id":  
            "name": {
               "bsonType": "string",
               "description": "unique index, string from 3 to 15 characters",
               "minLength": 3,
               "maxLength": 15
            },
            "price": {
               "bsonType": "number",
               "description": "float price as number from 1 to 10000",
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
               "bsonType": "int",
               "description": "integer number of boks as number from 1 to 10, default is 1",
               "minimum": 1,
               "maximum": 10
               # "default": 1
            },
            "image": {
               "bsonType": "string",
               "description": "image path as string from 5 to 150 characters",
            #    "default": "default.png",
               "minLength": 5,
               "maxLength": 150
            },
            "pages": {
               "bsonType": "int",
               "description": "integer number of book pages from 10 to 5000",
               "minimum": 10,
               "maximum": 50000
            }
          }
      }
    }

users_v = {
      "$jsonSchema": {
          "bsonType": "object",
          "required": [ "username", "password", "email", "role" ],
          "properties": {
            # "user_id":  
            "username": {
               "bsonType": "string",
               "description": "unique index, string from 3 to 20 characters",
               "minLength": 3,
               "maxLength": 20
            },
            "password": {
               "bsonType": "string",
               "description": "password is a string from 5 to 25 characters",
               "minLength": 5,
               "maxLength": 25
            },
            "email": {
               "bsonType": "string",
               "description": "string from 5 to 35 characters",
               "minLength": 5,
               "maxLength": 35
            },
            "role": {
               "bsonType": "int",
               "description": "integer number of boks as number from 1 to 10, default is 1",
               "minimum": 0,
               "maximum": 1
            },
            "book": {
               "bsonType": "string",
               "description": "image path as string from 5 to 150 characters",
               "minLength": 5,
               "maxLength": 150
            }
          }
      }
    }


#books_test
if "books_test" in db.list_collection_names():
   books_col = db["books_test"]
   books_col .create_index("name", unique=True)
else:
   books_col = db.create_collection("books_test", validator=books_v)

#users_test
if "users_test" in db.list_collection_names():
   users_col = db["users_test"]
   users_col .create_index("username", unique=True)
else:
   users_col = db.create_collection("users_test", validator=users_v)


#books testing
try:
    my_book_1 = { 
        "name": "Staki new q",
        "price": 20.34,
        "description": "neki glupi opis",
        "quantity": 7.45,
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

#users testing
try:
    my_user_1 = { 
        "username": "Aki",
        "password": "jidjejiejd",
        "email": "aki@gmail.com",
        "role": 0,
        "book": "lista ObjectID-eva",
    }
    doc1 = users_col.insert_one(my_user_1)
except Exception as e:
    print(e)

try:
    my_user_1 = { 
        "username": "Aki",
        "password": "jidjejiejd",
        "email": "aki@gmail.com",
        "role": 0,
        "book": "lista ObjectID-eva",
    }
    doc1 = users_col.insert_one(my_user_1)
except Exception as e:
    print(e)

# ts = datetime.datetime.now().strftime("%H:%M:%S")
# print(ts)

# for i in range(1,100):
#    new_doc = { 
#       "name": "Staki N"+str(i),
#       "price": i,
#       "description": "neki glupi opis",
#       "quantity": 8,
#       "pages": i*10,
#       "image": "staki"+str(i)+".jpg"
#    }
#    print(i)
#    books_col.insert_one(new_doc)

# ts = datetime.datetime.now().strftime("%H:%M:%S")
# print(ts)

# db.getCollectionInfos()
# db.getCollectionInfos( { name: "employees" } )

connection.close()





