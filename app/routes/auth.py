from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.security import LoginLocked, authenticate, csrf_protect, end_session, start_session
from app.web import redirect, render

router = APIRouter()


@router.get("/login")
def login_page(request: Request):
    if request.session.get("uid"):
        return redirect("/")
    return render(request, "login.html")


@router.post("/login", dependencies=[Depends(csrf_protect)])
def login(request: Request, email: str = Form(""), password: str = Form(""), db: Session = Depends(get_db)):
    try:
        user = authenticate(db, email, password)
    except LoginLocked as exc:
        return render(request, "login.html", status_code=429, email=email,
                      error=f"Too many failed attempts. Try again in {exc.minutes_left} minutes.")
    if user is None:
        return render(request, "login.html", status_code=401, email=email, error="Wrong email or password.")
    start_session(request, user)
    return redirect("/")


@router.post("/logout", dependencies=[Depends(csrf_protect)])
def logout(request: Request):
    end_session(request)
    return redirect("/login")
