from flask import Blueprint, abort, make_response, request, Response
from ..models.book import Book
from ..db import db


books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    
    new_book = Book(title=title, description=description)
    db.session.add(new_book)
    db.session.commit()

    response = {
        "id": new_book.id,
        "title": new_book.title,
        "description": new_book.description,
    }
    return response, 201

@books_bp.get("")
def get_all_books():
    query = db.select(Book)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.like(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))
        
    query = query.order_by(Book.id)
    books = db.session.scalars(query)
    
    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return books_response

@books_bp.get("/<id>")
def get_one_book(id):
    book = validate_book(id)
    return {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }

@books_bp.put("/<id>")
def update_book(id):
    book = validate_book(id)

    request_body = request.get_json()
    book.title = request_body["title"]
    book.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@books_bp.delete("/<id>")
def delete_book(id):
    book = validate_book(id)
    db.session.delete(book)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

def validate_book(id):
    try:
        book_id = int(id)
    except ValueError:
        response = {"message": f"book {id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Book).where(Book.id == id)
    book = db.session.scalar(query)
    if not book:
        response = {"message": f"book {id} not found"}
        abort(make_response(response, 404))

    return book
