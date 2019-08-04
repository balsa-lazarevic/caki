# mongo ds149742.mlab.com:49742/heroku_776l5bh4 -u connection_user -p cakiproject123
# mongodb://connection_user:cakiproject123@ds149742.mlab.com:49742/heroku_776l5bh4

import pymongo

MONGO_HOST = 'ds149742.mlab.com'
MONGO_PORT = 49742
MONGO_DB = 'heroku_776l5bh4'
MONGO_USER = 'connection_user'
MONGO_PASS = 'cakiproject123'
BOOKS_COLL = 'books'
USERS_COLL = 'users'


connection = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = connection[MONGO_DB]
db.authenticate(MONGO_USER, MONGO_PASS)
print(db.collection_names())

books_c = db[BOOKS_COLL]
users_c = db[USERS_COLL]

# connection.close()
