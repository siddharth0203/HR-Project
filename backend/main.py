from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
from models import Candidate, Job, Application
import database_models
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sample data
candidates = [
    Candidate(id=1, name="Siddharth", email="siddharth@example.com", phone_number=1234567890, current_status="Active", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Candidate(id=2, name="Yash", email="yash@example.com", phone_number=1234567891, current_status="Inactive", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Candidate(id=3, name="Priya", email="priya@example.com", phone_number=1234567892, current_status="Active", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Candidate(id=4, name="Abhi", email="abhi@example.com", phone_number=1234567893, current_status="Inactive", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Candidate(id=5, name="Anita", email="anita@example.com", phone_number=1234567894, current_status="Active", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
    Candidate(id=6, name="Rohit", email="rohit@example.com", phone_number=1234567895, current_status="Inactive", resume_link="https://drive.google.com/file/d/1PVIq4p1ua0G3zRRjQmERA4nSFwNWZzHY/view?usp=sharing"),
]
# Sample data 
jobs = [
    Job(id=1, title="Software Engineer", description="Develop and maintain software applications.", required_skills="Python, SQL, FastAPI", recruiter_id=101),
    Job(id=2, title="Data Analyst", description="Analyze and interpret complex data sets.", required_skills="SQL, Excel, Tableau", recruiter_id=102),
    Job(id=3, title="Project Manager", description="Oversee project planning and execution.", required_skills="Leadership, Communication, Agile", recruiter_id=103),
    Job(id=4, title="UX Designer", description="Design user-friendly interfaces and experiences.", required_skills="Figma, Adobe XD, User Research", recruiter_id=104),
    Job(id=5, title="DevOps Engineer", description="Manage and automate infrastructure and deployments.", required_skills="AWS, Docker, Kubernetes", recruiter_id=105),
    Job(id=6, title="QA Tester", description="Test software applications for bugs and issues.", required_skills="Selenium, JIRA, Test Planning", recruiter_id=106),
]

# Initialize database with sample data if empty
def init_db():
    db = SessionLocal()

    existing_count = db.query(database_models.Candidate).count()

    if existing_count == 0:
        for candidate in candidates:
            db.add(database_models.Candidate(**candidate.model_dump()))
        for job in jobs:
            db.add(database_models.Job(**job.model_dump()))
        db.commit()
        print("Database initialized.")
        
    db.close()

init_db()    

@app.get('/')
def read_root():
    return {"message": "Welcome to the HR Database API"}

@app.get("/candidates/")
def get_all_candidates(db: Session = Depends(get_db)):
    candidates = db.query(database_models.Candidate).all()
    return candidates


@app.get("/candidates/{candidate_id}")
def get_candidate_by_id(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(database_models.Candidate).filter(database_models.Candidate.id == candidate_id).first()
    if candidate:
        return candidate
    return {"error": "Candidate not found"}

@app.post("/candidates/")
def create_candidate(candidate: Candidate, db: Session = Depends(get_db)):
    db.add(database_models.Candidate(**candidate.model_dump()))
    db.commit()
    return {"message": "Candidate created successfully", "candidate": candidate}

@app.put("/candidates/{candidate_id}")
def update_candidate(candidate_id: int, candidate: Candidate, db: Session = Depends(get_db)):
    db_candidate = db.query(database_models.Candidate).filter(database_models.Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db_candidate.name = candidate.name
    db_candidate.email = candidate.email
    db_candidate.phone_number = candidate.phone_number
    db_candidate.current_status = candidate.current_status
    db_candidate.resume_link = candidate.resume_link
    db.commit()
    db.refresh(db_candidate)
    return {"message": "Candidate data updated successfully", "candidate": db_candidate}


@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    db_candidate = db.query(database_models.Candidate).filter(database_models.Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db.delete(db_candidate)
    db.commit()
    return {"message": "Candidate data deleted successfully"}
