import os
import json
import uuid

from fastapi import HTTPException
from PIL import Image
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.image import ProcessResponse
from app.database.crud import get_images_by_job, create_result, create_process, update_result
from app.schemas.crud import ResultCreate, ProcessCreate, ResultUpdate

TEMP_JSON_DIR = "temp_jsons"

async def get_image_histogram(job_id: str,     db: AsyncSession) -> ProcessResponse:
    os.makedirs(TEMP_JSON_DIR, exist_ok=True)
    
    process_data = ProcessCreate(job_id=job_id, name="histogram")
    process = await create_process(db, process_data)

    images = await get_images_by_job(db, job_id=job_id)

    for image in images:
        image_path = image.file_path

        result_data = ResultCreate(image_id = image.id, process_id=process.id)
        result = await create_result(db, result_data) 

        if not image_path or not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image not found")

        with Image.open(image_path) as image:
            if image.mode != 'RGB':
                image = image.convert('RGB')

            image_array = np.array(image)
            histogram_r, _ = np.histogram(image_array[:, :, 0], bins=256, range=(0, 256))
            histogram_g, _ = np.histogram(image_array[:, :, 1], bins=256, range=(0, 256))
            histogram_b, _ = np.histogram(image_array[:, :, 2], bins=256, range=(0, 256))

            histogram_data = {
                "histogram_r": histogram_r.tolist(),
                "histogram_g": histogram_g.tolist(),
                "histogram_b": histogram_b.tolist()
            }

            json_filename = f"{uuid.uuid4()}.json"
            json_filepath = os.path.join(TEMP_JSON_DIR, json_filename)

            print(json_filepath)
            with open(json_filepath, 'w') as json_file:
                json.dump(histogram_data, json_file)

            update_result_data = ResultUpdate(status="done", result_url=json_filepath)
            result = await update_result(db, result.id, update_result_data)
    
    
    return ProcessResponse(process_id=process.id)