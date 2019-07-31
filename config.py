import pymongo

client = pymongo.MongoClient("ds149742.mlab.com:49742/heroku_776l5bh4")
db = client["connection_user"]
books_col = db["books"]
users_col = db["users"]

