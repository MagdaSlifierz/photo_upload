from pydantic import BaseModel

class PhotoModel(BaseModel):
    photo_name: str
    photo_url: str
