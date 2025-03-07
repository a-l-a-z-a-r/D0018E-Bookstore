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

@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.form.get('search', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search_query:
        cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", 
                       (f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute("SELECT * FROM books")
    
    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', books=books, username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, password))
            conn.commit()
            flash("Registration successful! You can now log in.")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()
    
    return render_template('register.html')

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    if book:
        return render_template('book_detail.html', book=book, username=session.get('username'))
    return "Book not found", 404

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash("You need to log in first to view your cart.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT books.id, books.title, books.price, shopping_cart.quantity 
        FROM shopping_cart 
        JOIN books ON shopping_cart.book_id = books.id
        WHERE shopping_cart.user_id = %s
    """, (session['user_id'],))
    cart_items = cursor.fetchall()
    cursor.close()
    conn.close()

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('cart.html', cart=cart_items, total_price=total_price, username=session.get('username'))



@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    if 'user_id' not in session:
        flash("You need to log in first to buy books.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO shopping_cart (user_id, book_id, quantity) 
        VALUES (%s, %s, 1) 
        ON DUPLICATE KEY UPDATE quantity = quantity + 1
    """, (session['user_id'], book_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Book added to the cart!")
    return redirect(url_for('cart'))

@app.route('/need_login')
def need_login():
    return render_template('need_login.html', username=session.get('username'))

@app.route('/remove_from_cart/<int:book_id>')
def remove_from_cart(book_id):
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shopping_cart WHERE user_id = %s AND book_id = %s", (session['user_id'], book_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Book removed from the cart.")
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        flash("You need to register first.")
        return redirect(url_for('register'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shopping_cart WHERE user_id = %s", (session['user_id'],))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Checkout successful! Thank you for your purchase.")
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thankyou.html', username=session.get('username'))

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
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']  # Store admin status
            flash("Login successful!")
            return redirect(url_for('admin_dashboard' if user['is_admin'] else 'home'))
        else:
            flash("Invalid credentials.")
    
    return render_template('login.html')


@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        flash("Access denied.")
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin.html', users=users, books=books, username=session.get('username'))


@app.route('/admin/add_book', methods=['POST'])
def add_book():
    if not session.get('is_admin'):
        flash("Access denied.")
        return redirect(url_for('home'))
    
    title = request.form['title']
    author = request.form['author']
    price = request.form['price']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, price) VALUES (%s, %s, %s)", 
                   (title, author, price))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Book added successfully!")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete_book/<int:book_id>')
def delete_book(book_id):
    if not session.get('is_admin'):
        flash("Access denied.")
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Book deleted successfully.")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if not session.get('is_admin'):
        flash("Access denied.")
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("User deleted successfully.")
    return redirect(url_for('admin_dashboard'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("Logged out successfully.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
