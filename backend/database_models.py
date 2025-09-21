

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Candidate(Base):
    __tablename__ = "Candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone_number = Column(Integer)
    current_status = Column(String)
    resume_link = Column(String)

class Job(Base):
    __tablename__ = "Jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    required_skills = Column(String)
    recruiter_id = Column(Integer)

class Application(Base):
    __tablename__ = "Applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer)
    job_id = Column(Integer)