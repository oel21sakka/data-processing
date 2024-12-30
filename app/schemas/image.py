from pydantic import BaseModel
from typing import Optional, List

class ImageUploadResponse(BaseModel):
    image_id: str

class ImageResponse(BaseModel):
    width: int
    height: int

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