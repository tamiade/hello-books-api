from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", back_populates="books")
    genres = db.relationship("Genre", secondary="book_genre", backref="books")

    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description}

    @classmethod
    def from_dict(cls, book_data):
        new_book = cls(title=book_data["title"], description=book_data["description"])
        return new_book
