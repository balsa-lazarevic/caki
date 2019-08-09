import config

book_data = {
      "$jsonSchema": {
          "bsonType": "object",
          "required": ["name", "price"],
          "properties": {
            "name": {
               "bsonType": "string",
               "description": "must be a string and is required",
               "minLength": 3,
                "maxLength": 15
            },
            "description": {
               "bsonType": "string",
               "description": "must be a string and is optional",
               "minLength": 10,
                "maxLength": 150
            },
            "price": {
               "bsonType": "double",
               "description": "must be a float and is required",
               "minimum" : 1,
               "maximum": 10000
            },            
              "quantity": {
               "bsonType": "int",
               "description": "must be a int and is optional",
               "default" : 1,
                "minimum" : 1,
               "maximum": 10
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

