from pydantic import BaseModel
from typing import Optional, List

class JopResponse(BaseModel):
    job_id: int

class ProcessResponse(BaseModel):
    process_id: int

class ImageUploadResponse(BaseModel):
    image_id: int

class ResultResponse(BaseModel):
    result_id: int

class ImageManipulationRequest(BaseModel):
    resize_width: Optional[int] = None
    resize_height: Optional[int] = None
    crop_x: Optional[int] = None
    crop_y: Optional[int] = None
    crop_width: Optional[int] = None
    crop_height: Optional[int] = None
    convert_format: Optional[str] = None

class HistogramResponse(BaseModel):
    histogram_r: List[int]
    histogram_g: List[int]
    histogram_b: List[int]

class SegmentationResponse(BaseModel):
    segments: List[List[int]]