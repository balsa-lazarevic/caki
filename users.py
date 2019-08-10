users_v = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "password", "email", "role"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "unique index, string from 3 to 20 characters",
                "minLength": 3,
                "maxLength": 20
            },
            "password": {
                "bsonType": "string",
                "description": "password is a string from 5 to 25 characters written as SHA256 hash of 64 HEX characters",
                "minLength": 64,
                "maxLength": 64
            },
            "email": {
                "bsonType": "string",
                "description": "string from 5 to 35 characters",
                "minLength": 5,
                "maxLength": 35
            },
            "role": {
                "bsonType": "int",
                "description": "integer number of boks as number from 1 to 10, default is 1",
                "minimum": 0,
                "maximum": 1
            },
            "book": {
                "bsonType": "object",
                "description": "list of book object IDs",
            }
        }
    }
}
