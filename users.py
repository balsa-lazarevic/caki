import config
import pymongo

usr_data = {
      "$jsonSchema": {
          "bsonType": "object",
          "required": ["username", "password","email","role"],
          "properties": {
            "username": {
               "bsonType": "index",
               "description": "required",
               "minLength": 3,
                "maxLength": 20
            },
            "password": {
               "bsonType": "string",
               "description": "must be a string and is required",
               "minLength": 5,
                "maxLength": 25
            },
            "email": {
               "bsonType": "string",
               "pattern": "^.+\@.+$", 
               "description": "must be a valid string and is required",
               "minLength": 5,
                "maxLength": 35
            },            
              "role": {
               "bsonType": ["basic","admin"],
               "description": "must be a basic or admin and is optional",           
            },           
               "pages": {
               "bsonType": "int",
               "description": "must be a number and is optional",
                "minimum": 10,
               "maximum": 5000
            },            
          }
      }
    }

