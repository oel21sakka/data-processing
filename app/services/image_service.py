import os
import uuid
from typing import List, Optional

from fastapi import HTTPException, UploadFile
from PIL import Image

from app.schemas.image import (
    ImageUploadResponse,
    ImageResponse,
)

TEMP_IMAGE_DIR = "temp_images"

async def save_image(files: List[UploadFile]) -> List[ImageUploadResponse]:
    os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)
    responses = []
    for file in files:
        image_id = str(uuid.uuid4())

        _, file_extension = os.path.splitext(file.filename)

        image_path = os.path.join(TEMP_IMAGE_DIR, f"{image_id}{file_extension}")

        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())

        responses.append(ImageUploadResponse(image_id=image_id+file_extension))
    return responses

async def manipulate_image(
    image_id: str,
    resize_width: Optional[int],
    resize_height: Optional[int],
    crop_x: Optional[int],
    crop_y: Optional[int],
    crop_width: Optional[int],
    crop_height: Optional[int],
    convert_format: Optional[str]
) -> ImageResponse:
    image_path = os.path.join(TEMP_IMAGE_DIR, image_id)

    if not os.path.exists(image_path):
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

        width, height = image.size
        return ImageResponse(width=width, height=height)


