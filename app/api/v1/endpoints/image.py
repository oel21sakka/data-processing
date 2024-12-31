from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import List, Optional
from app.schemas.crud import ResultResponse
from app.services.image_histogram_service import get_image_histogram
from app.services.image_segmentation_service import get_image_segmentation
from app.services.image_service import (
    manipulate_image,
    save_image,
)
from app.schemas.image import (
    ProcessResponse,
    JopResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.database.crud import get_result_by_process

router = APIRouter()


@router.post("/upload", response_model=JopResponse)
async def upload_images(
    files: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)
):
    try:
        results = await save_image(files, db)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/process/{job_id}", response_model=ProcessResponse)
async def process_image(
    job_id: str,
    resize_width: Optional[int] = None,
    resize_height: Optional[int] = None,
    crop_x: Optional[int] = None,
    crop_y: Optional[int] = None,
    crop_width: Optional[int] = None,
    crop_height: Optional[int] = None,
    convert_format: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await manipulate_image(
            job_id,
            resize_width,
            resize_height,
            crop_x,
            crop_y,
            crop_width,
            crop_height,
            convert_format,
            db,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/histogram/{job_id}", response_model=ProcessResponse)
async def get_histogram(job_id: str, db: AsyncSession = Depends(get_db)):
    try:
        histogram = await get_image_histogram(job_id, db)
        return histogram
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/segmentation/{job_id}", response_model=ProcessResponse)
async def get_segmentation(job_id: str, db: AsyncSession = Depends(get_db)):
    try:
        segmentation = await get_image_segmentation(job_id, db)
        return segmentation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/results/{process_id}", response_model=list[ResultResponse])
async def view_results_by_process(process_id: int, db: AsyncSession = Depends(get_db)):
    try:
        results = await get_result_by_process(db, process_id)
        if not results:
            raise HTTPException(status_code=404, detail="No results found for this process")
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))