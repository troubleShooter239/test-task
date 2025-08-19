from pydantic import BaseModel, ConfigDict


class BaseOrm(BaseModel):
    model_config = ConfigDict(from_attributes=True)
