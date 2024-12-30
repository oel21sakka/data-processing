import os

from fastapi import HTTPException
from PIL import Image
import numpy as np
from skimage import segmentation

from app.schemas.image import (
    SegmentationResponse
)

TEMP_IMAGE_DIR = "temp_images"

async def get_image_segmentation(image_id: str) -> SegmentationResponse:
    original_image_path = os.path.join(TEMP_IMAGE_DIR, image_id)

    if not original_image_path:
        raise HTTPException(status_code=404, detail="Image not found")

    with Image.open(original_image_path) as image:
        if image.mode != 'RGB':
            image = image.convert('RGB')

        image_array = np.array(image)

        segments = segmentation.slic(image_array, n_segments=10, compactness=10, channel_axis=-1)

        segments_list = segments.tolist()

        return SegmentationResponse(segments=segments_list)