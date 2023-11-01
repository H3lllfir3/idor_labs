from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Query, Path, Body, Cookie, Header, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi import Cookie

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)


# Templates setup
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request, user: str = Cookie(None)):
    authenticated = False
    user_data = None

    if user:
    
        db = SessionLocal()
        user_data = db.query(User).filter(User.username == user).first()
        db.close()
        authenticated = True

    return templates.TemplateResponse("index.html", {"request": request, "authenticated": authenticated, "user_data": user_data})

@app.get("/login")
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/api/login")
async def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username, User.password == password).first()
    db.close()
    if user:
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key="user", value=user.username)
        return response
    raise HTTPException(status_code=400, detail="Login failed. Check your credentials.")

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("user")
    return response

@app.get("/api/user/{id}", response_model=dict)
async def profile_data(id: int):
    db = SessionLocal()
    current_user = db.query(User).filter(User.id == id).first()
    db.close()

    if current_user:
        user_data = {
            'username': current_user.username,
            'password': current_user.password,
            'name': current_user.name,
            'email': current_user.email
        }
        return user_data

    raise HTTPException(status_code=401, detail="Not authenticated or unauthorized")

@app.get("/profile", response_class=templates.TemplateResponse)
async def profile_template(request: Request, user: str = Cookie(None)):
    if user:
        db = SessionLocal()
        username = db.query(User).filter(User.username == user).first()
        db.close()
        if username:
            return templates.TemplateResponse("profile.html", {"request": request, "user": username})

    return RedirectResponse(url="/login", status_code=302)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
