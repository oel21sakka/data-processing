from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    pass

class ImageCreate(BaseModel):
    file_path: str
    job_id: int

class ProcessCreate(BaseModel):
    job_id: int

class ResultCreate(BaseModel):
    image_id: int
    process_id: int

class ResultUpdate(BaseModel):
    status: str
    result_url: str