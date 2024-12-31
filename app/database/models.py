from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    images = relationship("Image", back_populates="job")
    processes = relationship("Process", back_populates="job")

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    file_path = Column(String)
    job = relationship("Job", back_populates="images")
    results = relationship("Result", back_populates="image")

class Process(Base):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    name = Column(String)

    job = relationship("Job", back_populates="processes")
    results = relationship("Result", back_populates="process")

class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey('images.id'))
    process_id = Column(Integer, ForeignKey('processes.id'))
    status = Column(String, default="pending")
    result_url = Column(String)
    image = relationship("Image", back_populates="results")
    process = relationship("Process", back_populates="results")