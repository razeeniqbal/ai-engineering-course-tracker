from pathlib import Path

from fastapi import Depends, FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.routes import auth, episodes, modules
from app.routes import settings as settings_routes
from app.security import NotAuthenticated, csrf_protect, current_user
from app.services import NotFound
from app.web import is_htmx, redirect, render

CSP = ("default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; "
       "form-action 'self'; frame-ancestors 'none'; base-uri 'none'")


def create_app() -> FastAPI:
    app = FastAPI(title="Course Tracker", docs_url=None, redoc_url=None, openapi_url=None)

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("Content-Security-Policy", CSP)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        if settings.cookie_secure:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        if not request.url.path.startswith("/static"):
            response.headers["Cache-Control"] = "no-store"
        return response

    # Added after the headers middleware so it runs first and the session is ready for routes.
    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, session_cookie="ct_session",
                       max_age=settings.session_max_age, same_site="lax", https_only=settings.cookie_secure)

    app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

    @app.get("/healthz", include_in_schema=False)
    def healthz():
        return PlainTextResponse("ok")

    app.include_router(auth.router)
    protected = [Depends(current_user), Depends(csrf_protect)]
    for module in (episodes, modules, settings_routes):
        app.include_router(module.router, dependencies=protected)

    @app.exception_handler(NotAuthenticated)
    async def not_authenticated(request: Request, exc: NotAuthenticated):
        if is_htmx(request):
            return PlainTextResponse("", status_code=401, headers={"HX-Redirect": "/login"})
        return redirect("/login")

    @app.exception_handler(NotFound)
    async def not_found(request: Request, exc: NotFound):
        return render(request, "error.html", status_code=404, message="That page doesn't exist.")

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        if is_htmx(request):
            return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
        return render(request, "error.html", status_code=exc.status_code, message=str(exc.detail))

    return app


app = create_app()
