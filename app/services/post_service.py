from sqlalchemy.orm import Session

from app.models.post import Post


def get_all_posts(db: Session, skip: int = 0, limit: int = 10):
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    count = db.query(Post).count()
    return posts, count


def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def create_post(db: Session, title: str, author: str, content: str = "", published: bool = False):
    post = Post(title=title, author=author, content=content, published=published)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post_id: int, title: str, author: str, content: str = "", published: bool = False):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    post.title = title
    post.author = author
    post.content = content
    post.published = published
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False
