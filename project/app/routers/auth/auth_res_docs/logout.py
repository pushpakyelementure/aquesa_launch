from fastapi import status

responses = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "User Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Bad Request",
                }
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Internal Server Error",
                }
            },
        },
    },
}
