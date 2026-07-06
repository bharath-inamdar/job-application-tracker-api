from fastapi import FastAPI, HTTPException, Depends

from app.database import create_database_tables as init_database_tables, get_db
from app.models import JobApplication
from app.db_models import Application
from sqlalchemy.orm import Session

app = FastAPI()


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
def create_application(application: JobApplication, db: Session = Depends(get_db)):
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
@app.get("/applications")
def get_applications(db: Session = Depends(get_db)):
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
@app.delete("/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    db_application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    deleted_data = {
        "id": db_application.id,
        "company": db_application.company,
        "role": db_application.role,
        "status": db_application.status,
    }

    db.delete(db_application)
    db.commit()

    return {
        "message": "Application deleted successfully",
        "deleted": deleted_data,
    }
@app.put("/applications/{application_id}")
def update_application(application_id: int, application: JobApplication, db: Session = Depends(get_db)):
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