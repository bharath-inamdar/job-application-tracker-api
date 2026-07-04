from fastapi import FastAPI
from app.models import JobApplication
app = FastAPI()
applications = []

@app.get("/")
def home():
    return {"message": "Hello Boss!"}

@app.get("/about")
def about():
    return {
        "name": "Bharath",
        "college": "MSRIT",
        "goal": "12-20 LPA"
    }
@app.get("/dream")
def dream():
    return {
        "goal": "12-20 LPA",
        "company_type": "Product Based"
    }
@app.get("/companies")
def companies():
    return [
        "Google",
        "Microsoft",
        "Amazon",
        "Atlassian",
        "Adobe"
    ]
@app.get("/skills")
def skills():
    return {
  "language": "Python",
  "framework": "FastAPI",
  "database": "PostgreSQL"
}
@app.post("/applications")
def create_application(application: JobApplication):
    applications.append(application.model_dump())

    return {
        "message": "Application added successfully"
    }
@app.get("/applications")
def get_applications():
    return applications