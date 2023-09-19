import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from models import User, Gender, Role, UserUpdateRequest
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

async def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

DB = sqlite3.connect(':memory:')

@app.on_event("startup")
async def init_db():
    cur = DB.cursor()
    cur.execute("CREATE TABLE users (user text, password text)")
    cur.execute("INSERT INTO users VALUES ('admin', 'admin')")
    DB.commit()

@app.get("/login")
async def login(user: str, password: str):
    cur = DB.cursor()
    cur.execute("SELECT * FROM users WHERE user = '%s' AND password = '%s'" % (user, password))
    user = cur.fetchone()
    cur.close()
    if user:
        return '👋 Welcome back %s!' % (user[0],)
    return '🚨Bad credentials!'

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/users")
async def fetch_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@app.post("/api/v1/users")
async def register_user(user: User, db: Session = Depends(get_db)):

    user_model = models.Users()
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.middle_name = user.middle_name
    user_model.gender = user.gender
    user_model.role = user.role

    db.add(user_model)
    db.commit()

    return user

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404, 
            detail=f"User with id: {user_id} does not exist!"
        )
    
    db.query(models.Users).filter(models.Users.id == user_id).delete()

    db.commit()

@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: int, user: UserUpdateRequest, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"The user with the id: {user_id} does not exist!"
        )


    if user.first_name is not None:
        user_model.first_name = user.first_name
    if user.last_name is not None:
        user_model.last_name = user.last_name
    if user.middle_name is not None:
        user_model.middle_name = user.middle_name
    if user.role is not None:
        user_model.role = user.role

    db.add(user_model)
    db.commit()

    return user
