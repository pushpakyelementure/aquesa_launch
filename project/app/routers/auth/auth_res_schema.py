from pydantic import BaseModel


class logout_response(BaseModel):
    detail: str
