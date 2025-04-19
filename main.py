from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import User, UserDetails
from auth import authenticate_user, create_user, get_password_hash
import uvicorn
from datetime import datetime

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse("/user/form", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "success": request.session.pop("success", None), "error": request.session.pop("error", None)})

@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "success": request.session.pop("success", None), "error": request.session.pop("error", None)})

@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if user:
        request.session["user_id"] = user.id
        request.session["is_admin"] = user.is_admin
        request.session["success"] = "Login successful!"
        if user.is_admin:
            return RedirectResponse("/admin/dashboard", status_code=302)
        else:
            return RedirectResponse("/user/form", status_code=302)
    request.session["error"] = "Invalid credentials"
    return RedirectResponse("/login", status_code=302)

@app.get("/signup", response_class=HTMLResponse)
def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "success": request.session.pop("success", None), "error": request.session.pop("error", None)})

@app.post("/signup", response_class=HTMLResponse)
def signup_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        request.session["error"] = "Username already exists"
        return RedirectResponse("/signup", status_code=302)
    create_user(db, username, password)
    request.session["success"] = "Signup successful! Please login."
    return RedirectResponse("/login", status_code=302)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)

@app.get("/user/form", response_class=HTMLResponse)
def user_form_get(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=302)
    user = db.query(User).filter(User.id == user_id).first()
    details = user.details if user and user.details else None
    return templates.TemplateResponse("user_form.html", {"request": request, "details": details or {}, "success": request.session.pop("success", None), "error": request.session.pop("error", None)})

@app.post("/user/form", response_class=HTMLResponse)
def user_form_post(request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    current_semester: str = Form(...),
    tenth_percentage: float = Form(...),
    twelfth_percentage: float = Form(...),
    graduation_percentage: float = Form(...),
    specialization: str = Form(...),
    experience_status: str = Form(...),
    db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/login", status_code=302)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse("/login", status_code=302)
    details = user.details
    if not details:
        details = UserDetails(user_id=user.id)
        db.add(details)
        msg = "Details created!"
    else:
        msg = "Details updated!"
    details.first_name = first_name
    details.last_name = last_name
    details.email = email
    details.mobile = mobile
    details.dob = datetime.strptime(dob, "%Y-%m-%d").date()
    details.gender = gender
    details.current_semester = current_semester
    details.tenth_percentage = tenth_percentage
    details.twelfth_percentage = twelfth_percentage
    details.graduation_percentage = graduation_percentage
    details.specialization = specialization
    details.experience_status = experience_status
    db.commit()
    request.session["success"] = msg
    return RedirectResponse("/user/form", status_code=302)

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, search: str = "", db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse("/login", status_code=302)
    query = db.query(User).filter(User.is_admin == False)
    if search:
        query = query.join(UserDetails).filter(
            (User.username.contains(search)) |
            (UserDetails.first_name.contains(search)) |
            (UserDetails.last_name.contains(search)) |
            (UserDetails.email.contains(search))
        )
    users = query.all()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "users": users, "search": search, "success": request.session.pop("success", None), "error": request.session.pop("error", None)})

@app.get("/admin/user/{user_id}", response_class=HTMLResponse)
def admin_view_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse("/login", status_code=302)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse("/admin/dashboard", status_code=302)
    details = user.details
    return templates.TemplateResponse("admin_view.html", {"request": request, "user": user, "details": details})

@app.get("/admin/user/{user_id}/edit", response_class=HTMLResponse)
def admin_edit_user_get(request: Request, user_id: int, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse("/login", status_code=302)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse("/admin/dashboard", status_code=302)
    details = user.details or None
    return templates.TemplateResponse("admin_edit.html", {"request": request, "user": user, "details": details or {}, "success": request.session.pop("success", None), "error": request.session.pop("error", None)})

@app.post("/admin/user/{user_id}/edit", response_class=HTMLResponse)
def admin_edit_user_post(request: Request, user_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    current_semester: str = Form(...),
    tenth_percentage: float = Form(...),
    twelfth_percentage: float = Form(...),
    graduation_percentage: float = Form(...),
    specialization: str = Form(...),
    experience_status: str = Form(...),
    db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse("/login", status_code=302)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse("/admin/dashboard", status_code=302)
    details = user.details
    if not details:
        details = UserDetails(user_id=user.id)
        db.add(details)
        msg = "User details created!"
    else:
        msg = "User details updated!"
    details.first_name = first_name
    details.last_name = last_name
    details.email = email
    details.mobile = mobile
    details.dob = datetime.strptime(dob, "%Y-%m-%d").date()
    details.gender = gender
    details.current_semester = current_semester
    details.tenth_percentage = tenth_percentage
    details.twelfth_percentage = twelfth_percentage
    details.graduation_percentage = graduation_percentage
    details.specialization = specialization
    details.experience_status = experience_status
    db.commit()
    request.session["success"] = msg
    return RedirectResponse(f"/admin/user/{user_id}/edit", status_code=302)

@app.get("/admin/user/{user_id}/delete")
def admin_delete_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse("/login", status_code=302)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        request.session["success"] = "User deleted!"
    return RedirectResponse("/admin/dashboard", status_code=302)

@app.get("/create-admin")
def create_admin(request: Request, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == "admin@149gmail.com").first():
        request.session["error"] = "Admin already exists."
        return RedirectResponse("/login", status_code=302)
    create_user(db, "admin@149gmail.com", "Admin@149", is_admin=True)
    request.session["success"] = "Admin created. You can now login as admin."
    return RedirectResponse("/login", status_code=302)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7860, reload=True)
