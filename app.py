from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  
    'password': 'Pajalsta1313',
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
        cursor.execute("""
            SELECT books.*, 
                   ROUND(AVG(ratings.rating), 1) AS avg_rating, 
                   COUNT(ratings.rating) AS total_ratings
            FROM books 
            LEFT JOIN ratings ON books.id = ratings.book_id
            WHERE books.title LIKE %s OR books.author LIKE %s
            GROUP BY books.id
        """, (f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute("""
            SELECT books.*, 
                   ROUND(AVG(ratings.rating), 1) AS avg_rating, 
                   COUNT(ratings.rating) AS total_ratings
            FROM books 
            LEFT JOIN ratings ON books.id = ratings.book_id
            GROUP BY books.id
        """)
    
    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', books=books, username=session.get('username'))


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch book details
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        return "Book not found", 404  # Handle invalid book IDs

    # Fetch average rating
    cursor.execute("""
        SELECT ROUND(AVG(rating), 1) AS avg_rating, COUNT(rating) AS total_ratings
        FROM ratings WHERE book_id = %s
    """, (book_id,))
    rating_data = cursor.fetchone()
    avg_rating = rating_data['avg_rating'] if rating_data['avg_rating'] is not None else "★"
    total_ratings = rating_data['total_ratings']

    # Fetch comments (including replies)
    cursor.execute("""
        WITH RECURSIVE comment_tree AS (
            SELECT id, book_id, user_id, parent_comment_id, comment_text, created_at 
            FROM comments 
            WHERE book_id = %s AND parent_comment_id IS NULL
            UNION ALL
            SELECT c.id, c.book_id, c.user_id, c.parent_comment_id, c.comment_text, c.created_at 
            FROM comments c 
            JOIN comment_tree ct ON c.parent_comment_id = ct.id
        ) 
        SELECT comment_tree.*, users.username 
        FROM comment_tree 
        JOIN users ON comment_tree.user_id = users.id 
        ORDER BY created_at ASC;
    """, (book_id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('book_detail.html', book=book, comments=comments, avg_rating=avg_rating, total_ratings=total_ratings, username=session.get('username'))

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch book details
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        return "Book not found", 404  # Handle invalid book IDs

    # Handle comment submission
    if request.method == 'POST' and 'comment' in request.form:
        if 'user_id' not in session:
            flash("You need to log in to comment.")
            return redirect(url_for('login'))

        comment_text = request.form['comment']
        parent_comment_id = request.form.get('parent_comment_id', None)

        print(f"DEBUG: Adding comment - book_id: {book_id}, user_id: {session['user_id']}, parent_id: {parent_comment_id}, text: {comment_text}")

        cursor.execute(
            "INSERT INTO comments (book_id, user_id, parent_comment_id, comment_text) VALUES (%s, %s, %s, %s)",
            (book_id, session['user_id'], parent_comment_id, comment_text)
        )
        conn.commit()
        flash("Comment added successfully!")

        # Reload page after posting comment
        return redirect(url_for('book_detail', book_id=book_id))

    # Fetch average rating
    cursor.execute("""
        SELECT ROUND(AVG(rating), 1) AS avg_rating, COUNT(rating) AS total_ratings
        FROM ratings WHERE book_id = %s
    """, (book_id,))
    rating_data = cursor.fetchone()
    avg_rating = rating_data['avg_rating'] if rating_data['avg_rating'] is not None else "★"
    total_ratings = rating_data['total_ratings']

    # Fetch comments (including replies)
    cursor.execute("""
        WITH RECURSIVE comment_tree AS (
            SELECT id, book_id, user_id, parent_comment_id, comment_text, created_at 
            FROM comments 
            WHERE book_id = %s AND parent_comment_id IS NULL
            UNION ALL
            SELECT c.id, c.book_id, c.user_id, c.parent_comment_id, c.comment_text, c.created_at 
            FROM comments c 
            JOIN comment_tree ct ON c.parent_comment_id = ct.id
        ) 
        SELECT comment_tree.*, users.username 
        FROM comment_tree 
        JOIN users ON comment_tree.user_id = users.id 
        ORDER BY created_at ASC;
    """, (book_id,))
    comments = cursor.fetchall()

    print(f"DEBUG: Fetched {len(comments)} comments")  # Debugging

    cursor.close()
    conn.close()

    return render_template('book_detail.html', book=book, comments=comments, avg_rating=avg_rating, total_ratings=total_ratings, username=session.get('username'))


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


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch book details
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        return "Book not found", 404

    # Fetch average rating
    cursor.execute("""
        SELECT ROUND(AVG(rating), 1) AS avg_rating, COUNT(rating) AS total_ratings
        FROM ratings WHERE book_id = %s
    """, (book_id,))
    rating_data = cursor.fetchone()
    avg_rating = rating_data['avg_rating'] if rating_data['avg_rating'] is not None else "No ratings yet"
    total_ratings = rating_data['total_ratings']

    # Fetch comments (same as before)
    cursor.execute("""
        WITH RECURSIVE comment_tree AS (
            SELECT id, book_id, user_id, parent_comment_id, comment_text, created_at 
            FROM comments 
            WHERE book_id = %s AND parent_comment_id IS NULL
            UNION ALL
            SELECT c.id, c.book_id, c.user_id, c.parent_comment_id, c.comment_text, c.created_at 
            FROM comments c 
            JOIN comment_tree ct ON c.parent_comment_id = ct.id
        ) 
        SELECT comment_tree.*, users.username 
        FROM comment_tree 
        JOIN users ON comment_tree.user_id = users.id 
        ORDER BY created_at ASC;
    """, (book_id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('book_detail.html', book=book, comments=comments, avg_rating=avg_rating, total_ratings=total_ratings, username=session.get('username'))


@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash("You need to log in first to view your cart.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch books in cart, grouped by book_id
    cursor.execute("""
        SELECT books.id, books.title, books.price, books.author, shopping_cart.quantity 
        FROM shopping_cart 
        JOIN books ON shopping_cart.book_id = books.id
        WHERE shopping_cart.user_id = %s
    """, (session['user_id'],))
    
    cart_items = cursor.fetchall()
    cursor.close()
    conn.close()

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('cart.html', cart=cart_items, total_price=total_price, username=session.get('username'))

@app.route('/update_cart/<int:book_id>/<string:action>')
def update_cart(book_id, action):
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if action == "increase":
        cursor.execute("UPDATE shopping_cart SET quantity = quantity + 1 WHERE user_id = %s AND book_id = %s",
                       (session['user_id'], book_id))
    
    elif action == "decrease":
        # Ensure quantity doesn't go below 1
        cursor.execute("SELECT quantity FROM shopping_cart WHERE user_id = %s AND book_id = %s", 
                       (session['user_id'], book_id))
        quantity = cursor.fetchone()
        
        if quantity and quantity[0] > 1:
            cursor.execute("UPDATE shopping_cart SET quantity = quantity - 1 WHERE user_id = %s AND book_id = %s",
                           (session['user_id'], book_id))
        else:
            cursor.execute("DELETE FROM shopping_cart WHERE user_id = %s AND book_id = %s", 
                           (session['user_id'], book_id))  # Remove if quantity is 1

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('cart'))


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
        flash("You need to log in first.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get total price
    cursor.execute("""
        SELECT SUM(books.price * shopping_cart.quantity) 
        FROM shopping_cart 
        JOIN books ON shopping_cart.book_id = books.id
        WHERE shopping_cart.user_id = %s
    """, (session['user_id'],))
    total_price = cursor.fetchone()[0]

    if total_price is None:
        flash("Your cart is empty.")
        return redirect(url_for('cart'))

    # Create new order
    cursor.execute("INSERT INTO orders (user_id, total_price) VALUES (%s, %s)", 
                   (session['user_id'], total_price))
    order_id = cursor.lastrowid

    # Move cart items to order_items
    cursor.execute("""
        INSERT INTO order_items (order_id, book_id, quantity, price)
        SELECT %s, book_id, quantity, price 
        FROM shopping_cart 
        JOIN books ON shopping_cart.book_id = books.id
        WHERE shopping_cart.user_id = %s
    """, (order_id, session['user_id']))

    # Clear cart
    cursor.execute("DELETE FROM shopping_cart WHERE user_id = %s", (session['user_id'],))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Checkout successful! Your order has been placed.")
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch user orders
    cursor.execute("""
        SELECT orders.id, orders.total_price, orders.created_at 
        FROM orders
        WHERE orders.user_id = %s
        ORDER BY orders.created_at DESC
    """, (session['user_id'],))
    user_orders = cursor.fetchall()

    # Fetch order items
    order_items = {}
    for order in user_orders:
        cursor.execute("""
            SELECT books.title, books.author, order_items.quantity, order_items.price 
            FROM order_items
            JOIN books ON order_items.book_id = books.id
            WHERE order_items.order_id = %s
        """, (order['id'],))
        order_items[order['id']] = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('orders.html', orders=user_orders, order_items=order_items, username=session.get('username'))

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

        # Fetch user from database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if user and user['password'] == password:  # Ensure password check is correct
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user.get('is_admin', 0)  # Handle missing is_admin key
            
            flash("Login successful!")
            return redirect(url_for('home'))
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



@app.route('/rate_book/<int:book_id>', methods=['POST'])
def rate_book(book_id):
    if 'user_id' not in session:
        flash("You need to log in to rate books.")
        return redirect(url_for('login'))

    rating = int(request.form['rating'])  # Get rating from form input

    if rating < 1 or rating > 5:
        flash("Invalid rating. Please choose between 1 and 5 stars.")
        return redirect(url_for('book_detail', book_id=book_id))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert or update rating (ensures one rating per user per book)
    cursor.execute("""
        INSERT INTO ratings (book_id, user_id, rating) 
        VALUES (%s, %s, %s) 
        ON DUPLICATE KEY UPDATE rating = VALUES(rating)
    """, (book_id, session['user_id'], rating))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Your rating has been submitted!")
    return redirect(url_for('book_detail', book_id=book_id))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("Logged out successfully.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
