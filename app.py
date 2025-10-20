from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import hashlib
import uuid
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['DATABASE'] = 'laundry.db'

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_admin BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Orders table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            service_type TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            pickup_option TEXT DEFAULT 'pickup',
            total_items INTEGER DEFAULT 0,
            total_price DECIMAL(10,2) DEFAULT 0.00,
            tshirts INTEGER DEFAULT 0,
            shorts INTEGER DEFAULT 0,
            pants INTEGER DEFAULT 0,
            caps INTEGER DEFAULT 0,
            socks INTEGER DEFAULT 0,
            towels INTEGER DEFAULT 0,
            bedsheets INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_order_number():
    return f"ML{str(uuid.uuid4().int)[:8]}"

# Pricing configuration
PRICING = {
    'washing': {
        'tshirts': 200,
        'shorts': 250,
        'pants': 300,
        'caps': 150,
        'socks': 100,
        'towels': 350,
        'bedsheets': 500
    },
    'ironing': {
        'tshirts': 150,
        'shorts': 200,
        'pants': 250,
        'caps': 100,
        'socks': 80,
        'towels': 200,
        'bedsheets': 300
    }
}

def create_admin_user():
    conn = get_db_connection()
    try:
        admin_exists = conn.execute('SELECT * FROM users WHERE is_admin = TRUE').fetchone()
        if not admin_exists:
            hashed_password = hash_password('icui4cu2')
            conn.execute('INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)',
                        ('admin', 'admin@mitaschool.com', hashed_password, True))
            conn.commit()
            print("Admin user created: admin@mitaschool.com / icui4cu2")
        else:
            print("Admin user already exists")
    except sqlite3.Error as e:
        print(f"Error creating admin user: {e}")
    finally:
        conn.close()

# Initialize database before first request (compatible with Flask versions that lack the decorator)
def _initialize_database():
    init_db()
    create_admin_user()

# Try to register to run before the first request; if the attribute isn't available, run now.
try:
    app.before_first_request(_initialize_database)
except AttributeError:
    _initialize_database()

def create_admin_user():
    conn = get_db_connection()
    try:
        admin_exists = conn.execute('SELECT * FROM users WHERE is_admin = TRUE').fetchone()
        if not admin_exists:
            hashed_password = hash_password('icui4cu2')
            conn.execute('INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)',
                        ('admin', 'admin@mitaschool.com', hashed_password, True))
            conn.commit()
            print("Admin user created: admin@mitaschool.com / icui4cu2")
        else:
            print("Admin user already exists")
    except sqlite3.Error as e:
        print(f"Error creating admin user: {e}")
    finally:
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        
        conn = get_db_connection()
        
        try:
            hashed_password = hash_password(password)
            conn.execute('INSERT INTO users (username, email, password, phone, address) VALUES (?, ?, ?, ?, ?)',
                        (username, email, hashed_password, phone, address))
            conn.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                           (email, hash_password(password))).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            flash('Login successful!', 'success')
            
            if user['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT * FROM orders 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', orders=orders)

@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        service_type = request.form['service_type']
        pickup_option = request.form['pickup_option']
        
        # Item quantities
        items = {
            'tshirts': int(request.form.get('tshirts', 0)),
            'shorts': int(request.form.get('shorts', 0)),
            'pants': int(request.form.get('pants', 0)),
            'caps': int(request.form.get('caps', 0)),
            'socks': int(request.form.get('socks', 0)),
            'towels': int(request.form.get('towels', 0)),
            'bedsheets': int(request.form.get('bedsheets', 0))
        }
        
        # Calculate total items and price
        total_items = sum(items.values())
        
        if total_items == 0:
            flash('Please add at least one item!', 'error')
            return redirect(url_for('create_order'))
        
        # Calculate price based on service type
        total_price = 0
        for item, quantity in items.items():
            if service_type == 'washing':
                total_price += PRICING['washing'][item] * quantity
            elif service_type == 'ironing':
                total_price += PRICING['ironing'][item] * quantity
            elif service_type == 'both':
                total_price += (PRICING['washing'][item] + PRICING['ironing'][item]) * quantity
        
        # Create order
        conn = get_db_connection()
        order_number = generate_order_number()
        
        conn.execute('''
            INSERT INTO orders (order_number, user_id, service_type, pickup_option, total_items, total_price,
                              tshirts, shorts, pants, caps, socks, towels, bedsheets)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order_number, session['user_id'], service_type, pickup_option, total_items, total_price,
              items['tshirts'], items['shorts'], items['pants'], items['caps'], 
              items['socks'], items['towels'], items['bedsheets']))
        
        conn.commit()
        conn.close()
        
        flash(f'Order created successfully! Your order number is: {order_number}', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_order.html')

@app.route('/track_order', methods=['GET', 'POST'])
def track_order():
    if request.method == 'POST':
        order_number = request.form['order_number']
        
        conn = get_db_connection()
        order = conn.execute('''
            SELECT o.*, u.username 
            FROM orders o 
            JOIN users u ON o.user_id = u.id 
            WHERE o.order_number = ?
        ''', (order_number,)).fetchone()
        conn.close()
        
        if order:
            return render_template('order_details.html', order=order)
        else:
            flash('Order not found!', 'error')
    
    return render_template('track_order.html')

@app.route('/order/<order_number>')
def order_details(order_number):
    conn = get_db_connection()
    order = conn.execute('''
        SELECT o.*, u.username, u.phone, u.address 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        WHERE o.order_number = ?
    ''', (order_number,)).fetchone()
    conn.close()
    
    if not order:
        flash('Order not found!', 'error')
        return redirect(url_for('track_order'))
    
    return render_template('order_details.html', order=order)

# Admin Routes
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied!', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Statistics
    total_orders = conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
    pending_orders = conn.execute('SELECT COUNT(*) FROM orders WHERE status = "pending"').fetchone()[0]
    in_progress_orders = conn.execute('SELECT COUNT(*) FROM orders WHERE status = "in_progress"').fetchone()[0]
    completed_orders = conn.execute('SELECT COUNT(*) FROM orders WHERE status = "completed"').fetchone()[0]
    total_users = conn.execute('SELECT COUNT(*) FROM users WHERE is_admin = FALSE').fetchone()[0]
    
    # Recent orders
    recent_orders = conn.execute('''
        SELECT o.*, u.username 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        ORDER BY o.created_at DESC 
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    stats = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'in_progress_orders': in_progress_orders,
        'completed_orders': completed_orders,
        'total_users': total_users
    }
    
    return render_template('admin_dashboard.html', stats=stats, recent_orders=recent_orders)

@app.route('/admin/orders')
def admin_orders():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied!', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT o.*, u.username, u.phone 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        ORDER BY o.created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('admin_orders.html', orders=orders)

@app.route('/admin/update_order_status', methods=['POST'])
def update_order_status():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Access denied!'}), 403
    
    order_id = request.json['order_id']
    status = request.json['status']
    
    conn = get_db_connection()
    
    if status == 'completed':
        conn.execute('UPDATE orders SET status = ?, completed_at = CURRENT_TIMESTAMP WHERE id = ?', 
                    (status, order_id))
    else:
        conn.execute('UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', 
                    (status, order_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/admin/users')
def admin_users():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied!', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users WHERE is_admin = FALSE ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template('admin_users.html', users=users)

if __name__ == '__main__':
    # Ensure database is initialized
    if not os.path.exists(app.config['DATABASE']):
        print("Creating new database...")
        init_db()
        create_admin_user()
    else:
        # Check if tables exist, if not initialize
        conn = get_db_connection()
        try:
            conn.execute('SELECT 1 FROM users LIMIT 1')
            conn.execute('SELECT 1 FROM orders LIMIT 1')
            print("Database tables exist.")
        except sqlite3.OperationalError:
            print("Tables don't exist, initializing database...")
            conn.close()
            init_db()
        finally:
            conn.close()
    
    # Create admin user if doesn't exist
    create_admin_user()
    
    app.run(debug=True)