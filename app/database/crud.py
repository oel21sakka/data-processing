from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import Job, Image, Result, Process
from app.schemas.crud import ImageCreate, ResultCreate, ProcessCreate, ResultUpdate

async def create_job(db: AsyncSession) -> Job:
    db_job = Job()
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

async def get_job(db: AsyncSession, job_id: int) -> Job:
    result = await db.execute(select(Job).filter(Job.id == job_id))
    return result.scalars().first()

async def create_image(db: AsyncSession, image: ImageCreate) -> Image:
    db_image = Image(job_id=image.job_id, file_path=image.file_path)
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image

async def get_images_by_job(db: AsyncSession, job_id: int) -> list[Image]:
    result = await db.execute(select(Image).filter(Image.job_id == job_id))
    return result.scalars().all()

async def create_process(db: AsyncSession, process: ProcessCreate) -> Process:
    db_process = Process(job_id=process.job_id, name=process.name)
    db.add(db_process)
    await db.commit()
    await db.refresh(db_process)
    return db_process

async def create_result(db: AsyncSession, result: ResultCreate) -> Result:
    db_result = Result(image_id=result.image_id, process_id=result.process_id)
    db.add(db_result)
    await db.commit()
    await db.refresh(db_result)
    return db_result

async def get_result_by_process(db: AsyncSession, process_id: int) -> list[Result]:
    results = await db.execute(select(Result).filter(Result.process_id == process_id))
    return results.scalars().all()

async def update_result(db: AsyncSession, result_id: int, result_update: ResultUpdate) -> Result | None:
    result = await db.execute(select(Result).filter(Result.id == result_id))
    db_result = result.scalars().first()

    if not db_result:
        return None

    db_result.status = result_update.status
    db_result.result_url = result_update.result_url

    db.add(db_result)
    await db.commit()
    await db.refresh(db_result)

    return db_result