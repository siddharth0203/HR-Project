
from pydantic import BaseModel


class Candidate(BaseModel):
    id: int
    name: str
    email: str
    phone_number: int 
    current_status: str
    resume_link: str

class Job(BaseModel):
    id: int
    title: str
    description: str
    required_skills: str
    recruiter_id: int 

class Application(BaseModel):
    id: int
    candidate_id: int
    job_id: int
