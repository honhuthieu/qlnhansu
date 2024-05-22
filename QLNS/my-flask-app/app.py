from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Kết nối MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="book"
)

cursor = db.cursor(dictionary=True)

@app.route('/books', methods=['GET'])
def get_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.json
    sql = "INSERT INTO books (title, author) VALUES (%s, %s)"
    val = (new_book['title'], new_book['author'])
    cursor.execute(sql, val)
    db.commit()
    return jsonify(new_book), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    updated_book = request.json
    sql = "UPDATE books SET title=%s, author=%s WHERE id=%s"
    val = (updated_book['title'], updated_book['author'], id)
    cursor.execute(sql, val)
    db.commit()
    return jsonify(updated_book)

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    sql = "DELETE FROM books WHERE id=%s"
    val = (id,)
    cursor.execute(sql, val)
    db.commit()
    return '', 204


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cursor.fetchone()
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
