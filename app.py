from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
from config import Config
from routes.customer_routes import customer_bp
from routes.product_routes import product_bp
from routes.transaction_routes import transaction_bp
from flask import Blueprint
import pymysql
import bcrypt
from pymysql.cursors import DictCursor
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

app = Flask(__name__)
app.secret_key = "prima"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'

def get_db_connection():
    try:
        return pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            cursorclass=DictCursor
        )
    except pymysql.err.OperationalError:
        # If database doesn't exist, create it
        create_database()
        return get_db_connection()

def create_database():
    """Create database if it doesn't exist"""
    try:
        # Connect without specifying database
        conn = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD']
        )
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['MYSQL_DB']}")
        conn.commit()
        cur.close()
        conn.close()
        print("Database created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")

def create_table():
    """Create users table if it doesn't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        print("Users table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")


# Initialize database and table
create_table()
@app.route('/')
def index():
    return render_template("base.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    # Handle POST request - regular form submission
    email = request.form['email']
    password = request.form['password'].encode('utf-8')
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            if bcrypt.checkpw(password, user['password'].encode('utf-8')):
                session['name'] = user['name']
                session['email'] = user['email']
                # Redirect to home on successful login
                return redirect(url_for('index'))
            else:
                # Password doesn't match - show error on login page
                flash("Invalid email or password", "error")
                return render_template("login.html", error="Invalid credentials")
        else:
            # User not found - show error on login page
            flash("No account found with this email", "error")
            return render_template("login.html", error="User not found")
            
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        return render_template("login.html", error="Database error")

# Alternative: AJAX login endpoint (optional)
@app.route('/api/login', methods=['POST'])
def api_login():
    """AJAX endpoint for login"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password').encode('utf-8')
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            if bcrypt.checkpw(password, user['password'].encode('utf-8')):
                session['name'] = user['name']
                session['email'] = user['email']
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'redirect': url_for('home')
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid email or password'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'No account found with this email'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Database error: {str(e)}'
        })
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, hash_password))
            conn.commit()
            cur.close()
            conn.close()
            
            session['name'] = name
            session['email'] = email
            flash("Registration successful!", "success")
            return redirect(url_for('home'))
            
        except pymysql.err.IntegrityError:
            flash("Email already exists. Please use a different email.", "error")
            return render_template("register.html", error="Email exists")
        except Exception as e:
            flash(f"Registration error: {str(e)}", "error")
            return render_template("register.html", error="Registration failed")
        
@app.route('/customers-page')
def customers_page():
    """Customers management page"""
    return render_template('customers.html')

@app.route('/products-page')
def products_page():
    """Products management page"""
    return render_template('products.html')

@app.route('/transactions')
def transactions_page():
    """Transactions management page"""
    return render_template('transactions.html')

@app.route('/reports')
def reports_page():
    """Sales reports page"""
    return render_template('reports.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Flask API is running successfully'
    })
        
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('index'))

# Register blueprints
app.register_blueprint(customer_bp) 
app.register_blueprint(product_bp) 
app.register_blueprint(transaction_bp)

if __name__ == '__main__':
    print("🚀 Starting WAOW Workshop Flask Application...")
    print("📍 Homepage: http://localhost:5000")
    print("📍 Customers: http://localhost:5000/customers")
    print("📍 Products: http://localhost:5000/products")
    print("📍 Transactions: http://localhost:5000/transactions")
    print("📍 Reports: http://localhost:5000/reports")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='localhost', port=5000)