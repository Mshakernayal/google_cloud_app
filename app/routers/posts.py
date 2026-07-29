from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.post import PaginatedPosts, PostCreate, PostResponse, PostUpdate
from app.services import post_service

router = APIRouter(tags=["posts"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    posts, _ = post_service.get_all_posts(db)
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})


@router.get("/new", response_class=HTMLResponse)
def new_post_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "post": None})


@router.post("/new")
def create_post_page(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    content: str = Form(""),
    published: bool = Form(False),
    db: Session = Depends(get_db),
):
    post = post_service.create_post(db, title, author, content, published)
    return RedirectResponse(f"/posts/{post.id}", status_code=303)


@router.get("/posts/{post_id}", response_class=HTMLResponse)
def view_post_page(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = post_service.get_post_by_id(db, post_id)
    if not post:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("post.html", {"request": request, "post": post})


@router.get("/posts/{post_id}/edit", response_class=HTMLResponse)
def edit_post_form(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = post_service.get_post_by_id(db, post_id)
    if not post:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("form.html", {"request": request, "post": post})


@router.post("/posts/{post_id}/edit")
def update_post_page(
    request: Request,
    post_id: int,
    title: str = Form(...),
    author: str = Form(...),
    content: str = Form(""),
    published: bool = Form(False),
    db: Session = Depends(get_db),
):
    post = post_service.update_post(db, post_id, title, author, content, published)
    if not post:
        return RedirectResponse("/", status_code=303)
    return RedirectResponse(f"/posts/{post.id}", status_code=303)


@router.post("/posts/{post_id}/delete")
def delete_post_page(post_id: int, db: Session = Depends(get_db)):
    post_service.delete_post(db, post_id)
    return RedirectResponse("/", status_code=303)
