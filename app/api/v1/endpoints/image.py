from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from app.services.image_histogram_service import get_image_histogram
from app.services.image_segmentation_service import get_image_segmentation
from app.services.image_service import (
    manipulate_image,
    save_image,
)
from app.schemas.image import (
    ImageResponse,
    ImageUploadResponse,
    HistogramResponse,
    SegmentationResponse
)
router = APIRouter()

@router.post("/upload", response_model=List[ImageUploadResponse])
async def upload_images(files: List[UploadFile] = File(...)):
    try:
        results = await save_image(files)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/process/{image_id}", response_model=ImageResponse)
async def process_image(
    image_id: str,
    resize_width: Optional[int] = None,
    resize_height: Optional[int] = None,
    crop_x: Optional[int] = None,
    crop_y: Optional[int] = None,
    crop_width: Optional[int] = None,
    crop_height: Optional[int] = None,
    convert_format: Optional[str] = None
):
    try:
        result = await manipulate_image(
            image_id,
            resize_width,
            resize_height,
            crop_x,
            crop_y,
            crop_width,
            crop_height,
            convert_format
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/histogram/{image_id}", response_model=HistogramResponse)
async def get_histogram(image_id: str):
    try:
        histogram = await get_image_histogram(image_id)
        return histogram
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/segmentation/{image_id}", response_model=SegmentationResponse)
async def get_segmentation(image_id: str):
    try:
        segmentation = await get_image_segmentation(image_id)
        return segmentation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))