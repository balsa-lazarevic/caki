import pymongo

uri = 'mongodb://aida:aidacoinis96@ds149742.mlab.com:49742/heroku_776l5bh4'
try: 
    client = pymongo.MongoClient(uri) 
    print("Connected successfully!") 
except:   
    print("Could not connect to MongoDB!")

db = client.get_default_database()
books_col = db["books"]
users_col = db["users"]








