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
        books_response.append(book.to_dict())
    return jsonify(books_response)

def validate_book(book_id):
    try:
        book = int(book_id)
    except:
        abort(make_response({"message":f"Book {book_id} invalid"}, 400))

    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message":f"Book {book_id} not found"}, 404))

    return book

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    chosen_book = validate_book(book_id)

    return chosen_book.to_dict()

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    chosen_book = validate_book(book_id)
    request_body = request.get_json()

    chosen_book.title = request_body["title"]
    chosen_book.description = request_body["description"]

    db.session.commit()

    return make_response(f"Book {book_id} successfully updated")

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    chosen_book = validate_book(book_id)

    db.session.delete(chosen_book)
    db.session.commit()

    return make_response(f"Book {book_id} successfully deleted")




