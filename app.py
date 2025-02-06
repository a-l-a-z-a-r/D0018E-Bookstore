from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure key

# Sample book data
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 10.99, "image": "great_gatsby.jpg"},
    {"id": 2, "title": "1984", "author": "George Orwell", "price": 9.99, "image": "1984.jpg"},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 12.99, "image": "mockingbird.jpg"},
    {"id": 4, "title": "The Unbearable Lightness of Being", "author": "Milan Kundera", "price": 15.99, "image": "lightness.jpg"},
    {"id": 5, "title": "Don Quixote", "author": "Miguel de Cervantes", "price": 5.99, "image": "don_quixote.jpg"},
    {"id": 6, "title": "Anxious People", "author": "Fredrik Backman", "price": 7.99, "image": "anxious_people.jpg"},
]

@app.route('/')
def home():
    return render_template('index.html', books=books)

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    # Find the book by its ID
    for book in books:
        if book['id'] == book_id:
            return render_template('book_detail.html', book=book)

    # If the book is not found, return a 404 error
    return "Book not found", 404

@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    cart = session.get('cart', [])
    for book in books:
        if book['id'] == book_id:
            cart.append(book)
            break
    session['cart'] = cart
    flash("Book added to the cart!")
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:book_id>')
def remove_from_cart(book_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != book_id]
    session['cart'] = cart
    flash("Book removed from the cart.")
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    session.pop('cart', None)  # Clear the cart
    flash("Checkout successful! Thank you for your purchase.")
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
