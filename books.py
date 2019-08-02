import pymongo
import jsonschema
from jsonschema import validate

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
