import pytest
from app import create_app
from app import db
from app.models.book import Book
from flask.signals import request_finished


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def two_saved_books(app):
    #Arrange
    book_one = Book(title="Purple Hibiscus", description="Family and becoming")
    book_two = Book(title="Americanah", description="Immigration and becoming")

    db.session.add_all([book_one, book_two])
    db.session.commit()