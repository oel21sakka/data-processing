from pydantic import BaseModel

class JobCreate(BaseModel):
    pass

class ImageCreate(BaseModel):
    file_path: str
    job_id: int

class ProcessCreate(BaseModel):
    job_id: int
    name: str

class ResultCreate(BaseModel):
    image_id: int
    process_id: int

class ResultUpdate(BaseModel):
    status: str
    result_url: str

class ResultResponse(BaseModel):
    id: int
    status: str
    result_url: str
    image_id: int