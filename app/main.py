from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from app.database import create_database_tables as init_database_tables, get_db
from app.models import (
    JobApplication,
    UserRegister,
    ApplicationResponse,
    LoginResponse,
    UserRegisterResponse,
)
from app.db_models import Application, User
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
@app.post("/applications", response_model=ApplicationResponse)
def create_application(
    application: JobApplication,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_application = Application(
        company=application.company,
        role=application.role,
        status=application.status,
        applied_date=application.applied_date,
        job_link=application.job_link,
        notes=application.notes,
        user_id=current_user.id,
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return {
        "message": "Application added successfully",
        "id": db_application.id,
    }

# User registration endpoint
@app.post("/register", response_model=UserRegisterResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User registered successfully",
        "user_id": db_user.id,
        "username": db_user.username,
    }

# User login endpoint
@app.post("/login", response_model=LoginResponse)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
@app.get("/applications")
def get_applications(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_applications = (
        db.query(Application)
        .filter(Application.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": app.id,
            "company": app.company,
            "role": app.role,
            "status": app.status,
            "applied_date": app.applied_date,
            "job_link": app.job_link,
            "notes": app.notes,
        }
        for app in db_applications
    ]
@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_application = (
        db.query(Application)
        .filter(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
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
def update_application(
    application_id: int,
    application: JobApplication,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_application = (
        db.query(Application)
        .filter(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
        .first()
    )

    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    db_application.company = application.company
    db_application.role = application.role
    db_application.status = application.status
    db_application.applied_date = application.applied_date
    db_application.job_link = application.job_link
    db_application.notes = application.notes

    db.commit()
    db.refresh(db_application)

    return {
        "message": "Application updated successfully",
        "updated": {
            "id": db_application.id,
            "company": db_application.company,
            "role": db_application.role,
            "status": db_application.status,
            "applied_date": db_application.applied_date,
            "job_link": db_application.job_link,
            "notes": db_application.notes,
        },
    }