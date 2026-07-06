from fastapi import FastAPI, HTTPException

from app.database import create_database_tables as init_database_tables, SessionLocal
from app.models import JobApplication
from app.db_models import Application

app = FastAPI()
applications = []


@app.on_event("startup")
def create_database_tables() -> None:
    init_database_tables()

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
    db = SessionLocal()

    try:
        db_application = Application(
            company=application.company,
            role=application.role,
            status=application.status,
        )

        db.add(db_application)
        db.commit()
        db.refresh(db_application)

        return {
            "message": "Application added successfully",
            "id": db_application.id,
        }
    finally:
        db.close()
@app.get("/applications")
def get_applications():
    db = SessionLocal()

    try:
        db_applications = db.query(Application).all()

        return [
            {
                "id": app.id,
                "company": app.company,
                "role": app.role,
                "status": app.status,
            }
            for app in db_applications
        ]
    finally:
        db.close()
@app.delete("/applications/{index}")
def delete_application(index: int):
    if index < 0 or index >= len(applications):
        raise HTTPException(status_code=404, detail="Application not found")

    deleted_application = applications.pop(index)

    return {
        "message": "Application deleted successfully",
        "deleted": deleted_application
    }
@app.put("/applications/{application_id}")
def update_application(application_id: int, application: JobApplication):
    db = SessionLocal()

    try:
        db_application = (
            db.query(Application)
            .filter(Application.id == application_id)
            .first()
        )

        if db_application is None:
            raise HTTPException(status_code=404, detail="Application not found")

        db_application.company = application.company
        db_application.role = application.role
        db_application.status = application.status

        db.commit()
        db.refresh(db_application)

        return {
            "message": "Application updated successfully",
            "updated": {
                "id": db_application.id,
                "company": db_application.company,
                "role": db_application.role,
                "status": db_application.status,
            },
        }
    finally:
        db.close()