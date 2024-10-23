from fastapi import status

responses = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "This user is not a member of this community",  # Noqa
        "content": {
            "application/json": {
                "example": {
                    "detail": "This user is not a member of this community",  # Noqa
                }
            },
        },
    },
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Invalid Token/ Token Not Provided.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid Token or Token Not Provided",
                    "headers": {
                        "WWW-Authenticate": 'Bearer error="invalid_token"'
                    },  # Noqa
                }
            },
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "description": "You are not authorized to perform this action",
        "content": {
            "application/json": {
                "example": {
                    "detail": "You are not authorized to perform this action",
                }
            },
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Community User not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Community User not found",
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
