from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from faker import Faker 

app = FastAPI()


fake = Faker()

# In-memory database
users_db = {
    1: {
        "id": 1,
        "username": "alex",
        "email": "alex@email.com",
        "phone": "001-427-216-6063x8915",
        "address": "18647 Travis Unions\nNguyenhaven, ND 55081"
    },
    2: {
        "id": 1,
        "username": fake.user(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address()
    }
}
def get_user_data(user_id):
    if user_id == 1:
        return {
            "id": 1,
            "username": "alex",
            "email": "alex@email.com",
            "phone": "001-427-216-6063x8915", 
            "address": "18647 Travis Unions\nNguyenhaven, ND 55081"
        }
    else:
        return {
            "id": user_id,
            "username": fake.user().split(" ")[0],
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address()  
        }


class User(BaseModel):
    username: str
    password: str

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=templates.TemplateResponse)
async def index(request: Request):
    return {"request": request, "template": "index.html"}


@app.get("/profile/{user_id}", response_class=templates.TemplateResponse)
async def profile(request: Request, user_id: int):
    user_data = users_db.get(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return {"request": request, "template": "profile.html", "user": user_data}


@app.get("/login", response_class=templates.TemplateResponse)
async def login_page(request: Request):
    return {"request": request, "template": "login.html"}

@app.post("/login")
async def login(user: User, request: Request):
    if user.username == "alex" and user.password == "alex1234":
        request.session['user'] = user.username
        return RedirectResponse(url="/profile/1")
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
