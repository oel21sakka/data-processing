import os
import uuid
from typing import List, Optional

from fastapi import HTTPException, UploadFile
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.image import (
    ImageUploadResponse,
    ProcessResponse,
    JopResponse,
)
from app.database.crud import get_images_by_job, create_image, create_job, create_result, create_process, update_result
from app.schemas.crud import ImageCreate, ResultCreate, ProcessCreate, ResultUpdate
from dotenv import load_dotenv

load_dotenv()

TEMP_IMAGE_DIR = os.getenv("TEMP_IMAGE_DIR")

async def save_image(files: List[UploadFile], db: AsyncSession) -> List[ImageUploadResponse]:
    os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)

    job = await create_job(db)

    for file in files:
        image_id = str(uuid.uuid4())
        _, file_extension = os.path.splitext(file.filename)
        image_path = os.path.join(TEMP_IMAGE_DIR, f"{image_id}{file_extension}")

        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())

        image_data = ImageCreate(file_path=image_path, job_id=job.id)
        await create_image(db, image_data)

    return JopResponse(job_id=job.id)

async def manipulate_image(
    job_id: str,
    resize_width: Optional[int],
    resize_height: Optional[int],
    crop_x: Optional[int],
    crop_y: Optional[int],
    crop_width: Optional[int],
    crop_height: Optional[int],
    convert_format: Optional[str],
    db: AsyncSession
) -> ProcessResponse:
    process_data = ProcessCreate(job_id=job_id, name="manipulation")
    process = await create_process(db, process_data)

    images = await get_images_by_job(db, job_id=job_id)
    for image in images:
        image_path = image.file_path

        result_data = ResultCreate(image_id = image.id, process_id=process.id)
        result = await create_result(db, result_data) 

        if not image_path or not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image not found")

        with Image.open(image_path) as image:
            if resize_width and resize_height:
                image = image.resize((resize_width, resize_height))

            if crop_x is not None and crop_y is not None and crop_width and crop_height:
                image = image.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))

            new_image_id = str(uuid.uuid4())
            new_file_extension = f".{convert_format.lower()}" if convert_format else os.path.splitext(image_path)[1]
            new_image_path = os.path.join(TEMP_IMAGE_DIR, f"{new_image_id}{new_file_extension}")

            image.save(new_image_path, format=convert_format.upper() if convert_format else None)

            update_result_data = ResultUpdate(status="done", result_url=new_image_path)
            result = await update_result(db, result.id, update_result_data)
    
    return ProcessResponse(process_id=process.id)


