import os

from fastapi import HTTPException
from PIL import Image
import numpy as np

from app.schemas.image import (
    HistogramResponse,
)

TEMP_IMAGE_DIR = "temp_images"

async def get_image_histogram(image_id: str) -> HistogramResponse:
    original_image_path = os.path.join(TEMP_IMAGE_DIR, image_id)

    if not original_image_path:
        raise HTTPException(status_code=404, detail="Image not found")

    with Image.open(original_image_path) as image:
        if image.mode != 'RGB':
            image = image.convert('RGB')

        image_array = np.array(image)

        histogram_r, _ = np.histogram(image_array[:, :, 0], bins=256, range=(0, 256))
        histogram_g, _ = np.histogram(image_array[:, :, 1], bins=256, range=(0, 256))
        histogram_b, _ = np.histogram(image_array[:, :, 2], bins=256, range=(0, 256))

        return HistogramResponse(
            histogram_r=histogram_r.tolist(),
            histogram_g=histogram_g.tolist(),
            histogram_b=histogram_b.tolist()
        )
    