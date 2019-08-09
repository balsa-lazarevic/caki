import pymongo
from .books import *
from .users import *

uri = 'mongodb://aida:aidacoinis96@ds149742.mlab.com:49742/heroku_776l5bh4'
try: 
    client = pymongo.MongoClient(uri) 
    print("Connected successfully!") 
except:   
    print("Could not connect to MongoDB!")

db = client.get_default_database()
books_col = db["books"]
users_col = db["users"]

#Dodaje validatore
db.runCommand({
  "collMod": "books",
  "validator": book_data,
  "validationLevel": "moderate"
})

db.runCommand({
  "collMod": "users",
  "validator": users_v,
  "validationLevel": "moderate"
})