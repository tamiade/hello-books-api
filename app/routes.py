from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.book import Book
from app.models.author import Author


def validate_model(cls, model_id):
    try:
        model = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


# ************************************ CRUD ROUTES FOR BOOKS ********************************

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book.from_dict(request_body)

    db.session.add(new_book)
    db.session.commit()

    return jsonify(f"Book {new_book.title} successfully added"), 201


@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response)


@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    chosen_book = validate_model(Book, book_id)

    return chosen_book.to_dict()


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    chosen_book = validate_model(Book, book_id)
    request_body = request.get_json()

    try:
        chosen_book.title = request_body["title"]
        chosen_book.description = request_body["description"]
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400

    db.session.commit()
    return jsonify(f"Book #{book_id} successfully updated")


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    chosen_book = validate_model(Book, book_id)

    db.session.delete(chosen_book)
    db.session.commit()

    return jsonify(f"Book #{book_id} successfully deleted")


# ******************************* CRUD ROUTES FOR AUTHORS ******************************

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")


@authors_bp.route("", methods=["GET"])
def read_all_authors():
    authors = Author.query.all()

    authors_response = []
    for author in authors:
        authors_response.append(author.to_dict())

    return jsonify(authors_response)


@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author.from_dict(request_body)

    db.session.add(new_author)
    db.session.commit()

    return jsonify(f"Author {new_author.name} successfully created"), 201


# ***************************** NESTED ROUTES FOR BOOKS AND AUTHORS *********************************


@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):
    chosen_author = validate_model(Author, author_id)

    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author=chosen_author,
    )

    db.session.add(new_book)
    db.session.commit()

    return (
        jsonify(
            f"Book {new_book.title} by {new_book.author.name} successfully created"
        ),
        201,
    )


@authors_bp.route("/<author_id>/books", methods=["GET"])
def read_books(author_id):
    chosen_author = validate_model(Author, author_id)

    books_response = []
    for book in chosen_author.books:
        books_response.append(book.to_dict())

    return jsonify(books_response)
