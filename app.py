from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'diamond-store-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    
    # ADDRESS FIELDS
    shipping_address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    
    # CARD FIELDS
    card_holder = db.Column(db.String(100), nullable=True)
    card_number = db.Column(db.String(20), nullable=True)
    card_expiry = db.Column(db.String(5), nullable=True)
    card_cvv = db.Column(db.String(4), nullable=True)
    card_type = db.Column(db.String(20), nullable=True)
    
    is_guest = db.Column(db.Boolean, default=False)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='exhog').first():
            admin = User(username='exhog', email='admin@diamondstore.com', password=generate_password_hash('root'), is_admin=True)
            db.session.add(admin)
            db.session.commit()
            print("Admin user 'exhog' created (pass: root)")
        if Product.query.count() < 5:
            for i in range(5):
                p = Product(name=f"Diamond Ring #{i+1}", description="Beautiful diamond.", price=100.00 + (i*25), image=None)
                db.session.add(p)
            db.session.commit()

def get_cart():
    return session.get('cart', [])

def add_to_cart(product_id):
    cart = get_cart()
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            session['cart'] = cart
            return
    cart.append({'id': product_id, 'quantity': 1})
    session['cart'] = cart

def remove_from_cart(product_id):
    session['cart'] = [item for item in get_cart() if item['id'] != product_id]

def get_cart_total():
    total = 0
    for item in get_cart():
        product = Product.query.get(item['id'])
        if product:
            total += product.price * item['quantity']
    return total

@app.route('/')
def home():
    products = Product.query.limit(20).all()
    return render_template('home.html', products=products)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)

@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    for item in get_cart():
        product = Product.query.get(item['id'])
        if product:
            cart_items.append({'product': product, 'quantity': item['quantity']})
            total += product.price * item['quantity']
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/cart/add/<int:id>', methods=['POST'])
def cart_add(id):
    add_to_cart(id)
    flash('Item added to cart!', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/cart/remove/<int:id>', methods=['POST'])
def cart_remove(id):
    remove_from_cart(id)
    flash('Item removed.', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        cart = get_cart()
        if not cart:
            flash('Cart is empty!', 'warning')
            return redirect(url_for('cart'))
        
        total = get_cart_total()
        name = request.form.get('name')
        email = request.form.get('email')
        is_guest = request.form.get('is_guest') == 'true'
        
        # Get Address
        shipping_address = request.form.get('shipping_address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        country = request.form.get('country')
        
        # Get Card
        card_holder = request.form.get('card_holder')
        card_number = request.form.get('card_number')
        card_expiry = request.form.get('card_expiry')
        card_cvv = request.form.get('card_cvv')
        card_type = request.form.get('card_type')

        new_order = Order(
            customer_name=name, customer_email=email, total=total,
            shipping_address=shipping_address, city=city, state=state, zip_code=zip_code, country=country,
            card_holder=card_holder, card_number=card_number,
            card_expiry=card_expiry, card_cvv=card_cvv,
            card_type=card_type, is_guest=is_guest
        )
        db.session.add(new_order)
        db.session.commit()
        session['cart'] = []
        flash('Order placed! Check admin panel.', 'success')
        return redirect(url_for('home'))
    
    cart_items = []
    total = 0
    for item in get_cart():
        product = Product.query.get(item['id'])
        if product:
            cart_items.append({'product': product, 'quantity': item['quantity']})
            total += product.price * item['quantity']
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username exists.', 'error')
            return redirect(url_for('register'))
        new_user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Admins only.', 'error')
        return redirect(url_for('home'))
    products = Product.query.all()
    orders = Order.query.order_by(Order.date_ordered.desc()).all()
    return render_template('admin.html', products=products, orders=orders)

@app.route('/admin/product/add', methods=['POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin: return redirect(url_for('home'))
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    image_file = request.files.get('image')
    image_name = None
    if image_file and image_file.filename:
        image_name = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
    new_product = Product(name=name, description=description, price=price, image=image_name)
    db.session.add(new_product)
    db.session.commit()
    flash('Product added!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/product/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_product(id):
    if not current_user.is_admin: return redirect(url_for('home'))
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'info')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    os.makedirs('static/images', exist_ok=True)
    app.run(debug=False, port=5000, host='0.0.0.0')
