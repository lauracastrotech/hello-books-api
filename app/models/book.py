from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .author import Author

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")

    def to_dict(self):
        book_as_dict = {}
        book_as_dict["id"] = self.id
        book_as_dict["title"] = self.title
        book_as_dict["description"] = self.description

        return book_as_dict
    
    @classmethod
    def from_dict(cls, book_data):
        new_book = cls(title=book_data["title"], description=book_data["description"])
        # We could also use `Book` in place of the `cls` keyword  
        # The following declaration is equivalent to the one above
        # new_book = Book(title=book_data["title"],
        #                 description=book_data["description"])

        return new_book