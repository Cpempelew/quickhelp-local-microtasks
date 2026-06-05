from pydantic import BaseModel


class UpdatePosition(BaseModel):
    latitude: float
    longitude: float
