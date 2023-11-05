from pydantic import BaseModel

class PhotoModel(BaseModel):
    id: int
    photo_name: str
    photo_url: str
    is_deleted: bool