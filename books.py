books_v = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "price"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "unique index, string from 3 to 15 characters",
                "minLength": 3,
                "maxLength": 15
            },
            "price": {
                "bsonType": "number",
                "description": "float price as number from 1 to 10000",
                "minimum": float(1),
                "maximum": float(10000)
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
                # "default": "default.png",
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

