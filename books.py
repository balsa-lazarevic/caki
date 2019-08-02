
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from bson.json_util import dumps
import pymongo
from flask_jwt import JWT, jwt_required
from security import identity, authenticate
import json
from config.py import db

vv = {
      "$jsonSchema": {
          "bsonType": "object",
          "required": [ "name", "price"],
          "optional": [ "description", "image", "quantity"],
          "properties": {
            "name": {
               "bsonType": "string",
               "minLength": 3,
               "maxLength": 15
            },
            "price": {
               "bsonType": "number",
               "minimum": 1,
               "maximum": 10000
            },
            "description": {
               "bsonType": "string",
               "minLength": 10,
               "maxLength": 150
            },
            "quantity": {
               "bsonType": "number",
               "minLength": 1,
               "maxLength": 10
            }
          }
      }
    }

if "books" not in db.list_collection_names():
    coll = db.create_collection("books", validator=vv)
    coll.create_index("index", unique=True)
else:
    coll = db["books"]




# class Student(Resource):

#     def get(self, name):
#         try:
#             student = list(mycol.find({"name": name}))
#             if student:
#                 return dumps(student), 200
#             else:
#                 return {"message": "Student with this name not found."}, 404
#         except Exception as e:
#             return {"error": str(e)}, 400

#     @jwt_required()
#     def post(self, name): 
#         try:
#             # Ako dodamo force=True, nije neophodno da se salje Content-Type:"application/json"
#             # Ako dodamo silent=True, vraca umjesto greske None (null)
#             request_data = request.get_json() # ako ne setujemo u zahtjevu Content-Type:"application/json" ili posaljemo invalid JSON, greska
#             new_student = {
#                 "name": request_data["name"],
#                 "email": request_data["email"],
#                 "index": request_data["index"]
#             }
#             mycol.insert_one(new_student)
#             return dumps(new_student), 201
#         except Exception as e:
#             return {"error": str(e)}, 400
    
#     @jwt_required()
#     def delete(self, name):
#         try:
#             student = mycol.find_one_and_delete({"name": name})
#             if student:
#                 return {"message": "Student deleted."}, 200
#             else:
#                 return {"message": "Student with this name not found."}, 404
#         except Exception as e:
#             return {"error": str(e)}, 400
    
#     @jwt_required()
#     def put(self, name):
#         try:
#             '''
#             request_data = request.get_json()'''
#             student = list(mycol.find({"name": name}))
#             parser = reqparse.RequestParser()
#             is_required = False
#             if not student: # ako ne postoji
#                 is_required = True
#             else:
#                 student = student[0]
#             parser.add_argument("name", type=str, required=is_required)
#             parser.add_argument("email", type=str, required=is_required)
#             parser.add_argument("index", type=str, required=is_required)
#             # Pazite da parametre koje ovdje rucno ne dodate nece biti izdvojeni iz linka, npr. posaljete parametar another=1 => request_data["another"] -> KeyError
#             request_data = parser.parse_args()
            
#             new_student = {
#                 "name":request_data["name"] if request_data["name"] else student["name"] ,
#                 "email": request_data["email"] if request_data["email"] else student["email"],
#                 "index": request_data["index"] if request_data["index"] else student["index"]
#             }
            
#             if not student:
#                 mycol.insert_one(new_student)
#                 return dumps(new_student), 201
#             else:
#                 mycol.update_one({"name": name}, {"$set": new_student})
#                 return {"message": "Updated"}, 200

#         except Exception as e:
#             return {"error": str(e)}, 400
