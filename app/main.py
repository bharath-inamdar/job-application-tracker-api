from fastapi import FastAPI, HTTPException
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
@app.delete("/applications/{index}")
def delete_application(index: int):
    if index < 0 or index >= len(applications):
        raise HTTPException(status_code=404, detail="Application not found")

    deleted_application = applications.pop(index)

    return {
        "message": "Application deleted successfully",
        "deleted": deleted_application
    }
@app.put("/applications/{index}")
def update_application(index: int, application: JobApplication):
    if index < 0 or index >= len(applications):
        raise HTTPException(status_code=404, detail="Application not found")

    applications[index] = application.model_dump()

    return {
        "message": "Application updated successfully",
        "updated": applications[index]
    }