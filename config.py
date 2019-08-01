# mongo ds149742.mlab.com:49742/heroku_776l5bh4 -u connection_user -p cakiproject123
# mongodb://connection_user:cakiproject123@ds149742.mlab.com:49742/heroku_776l5bh4

import sys
import pymongo
from pymongo import MongoClient

connection = MongoClient("ds149742.mlab.com", 49742)
db = connection["heroku_776l5bh4"]
# MongoLab has user authentication
db.authenticate("connection_user", "cakiproject123")