import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import db
from datetime import datetime

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(sa.DateTime, default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.title!r}, fullname={self.author_id!r})"