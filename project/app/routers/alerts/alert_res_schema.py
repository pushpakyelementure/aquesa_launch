from pydantic import BaseModel


class create_res_model(BaseModel):
    user_id: str
    detail: str