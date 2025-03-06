def ExampleResponseModel(data, message):
    return {
        "description": message,
        "content": {
            "application/json": {
                "example": {
                    "success":True,
                    "data": data,
                    "status_code": 200,
                    "message": message,
                }
            }
        }
    }

def ExampleErrorResponseModel(code, message):
    return {
        "description": message,
        "content": {
            "application/json": {
                "example": {
                    "success": False, 
                    "status_code": code, 
                    "message": message
                }
            }
        }
    }

def ResponseModel(data, message):
    return {
        "success":True,
        "data": data,
        "status_code": 200,
        "message": message,
    }

def ErrorResponseModel(code, message):
    return {"success": False, "status_code": code, "message": message}

