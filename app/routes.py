from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.book import Book 

books_bp = Blueprint("books", __name__, url_prefix="/books")  

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"], description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(f"Book {new_book.title} successfully added", 201)


@books_bp.route("", methods=["GET"])
def read_all_books():
    books_response = []
    books = Book.query.all()
    for book in books:
        books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
    return jsonify(books_response)

