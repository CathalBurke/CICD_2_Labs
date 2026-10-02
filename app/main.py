from fastapi import FastAPI, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas import UserCreate, UserRead
from app.models import Base, UserDB 
from app.database import engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab 3 - FastAPI SQLAlchemy ")


@app.get("/health")
def health ():
    return {"status": "ok"}

@app.post(
    "api/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def add_user(new_user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(**new_user.model_dump())
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email or student id already exists",
        )

    return db_user
