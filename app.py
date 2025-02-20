from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure key

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Change if using a different user
    'password': 'Alazar@1234',  # Change to your MySQL password
    'database': 'bookstore'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    if book:
        return render_template('book_detail.html', book=book)
    return "Book not found", 404

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total_price = sum(float(item['price']) for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if book:
        cart = session.get('cart', [])
        cart.append(book)
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
    session.pop('cart', None)
    flash("Checkout successful! Thank you for your purchase.")
    return render_template('checkout.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials.")
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
