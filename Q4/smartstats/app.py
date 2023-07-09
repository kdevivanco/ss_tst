from flask import Flask, redirect, render_template, session ,flash
import psycopg2
from flask import jsonify, request
import pdb
from flask import flash
from models.user import User
from models.basket import Basket
from models.products import Product
from models.orders import Order
from models.basket_product import BasketProduct
from models.decorator import login_required
from flask_bcrypt import Bcrypt        

# from flask_paypal import PayPal


app = Flask(__name__)
# app.config.from_envvar('.env')

# paypal = PayPal(app)
#set up secret key
app.secret_key ='super secret key'
app.config['DATABASE'] = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres'
}


bcrypt = Bcrypt(app)

def pseudodecorator():
    if not session['user'] or session == None:
        return False
    else:
        return True
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logout')
# @login_required
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods = ["GET"])
def show_register():
    #if user in session
    return render_template('register.html')

@app.route('/reg', methods =["POST"])
def register():
    if User.email_free(request.form['email']):

        User.create(request.form,bcrypt)

    #outcomes 
        if True: 
            return redirect('/shop')
        else:
            return ('/register')
    else: 
        #error handling
        flash('Error')
        return redirect('/register')
    
@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    user = User.login(request.form,bcrypt)
    #if user in session 
    if user:
        session['user']={
            'id' : user.id,
            'name': user.first_name,
            'last_name': user.last_name,  
            'email': user.email
        }
        return redirect('/shop')
    else:
        #flash an error
        return redirect('/login')

@app.route('/add-product/<product_id>',methods=['POST'])
def add_product(product_id):
    quantity = request.form['quantity']
    client_id = session['user']['id']
    Basket.add_products(product_id,quantity,client_id)
    return redirect('/cart')
    
@app.route('/products/<category_id>')
def load_by_category(category_id):
    products = Product.get_by_category(category_id)
    return render_template('products.html', products = products)

@app.route('/product/<product_id>')
def load_product(product_id):
    product = Product.find_one(product_id)
    return render_template('product.html',product = product )
    

@app.route('/pay', methods=['POST'])
def pay():
    to_pay = Basket.get_price
    order = Order.create(session['user']['id'])

@app.route('/shop')
def show_shop():
    return render_template('home.html')

@app.route('/cart')
def show_cart():
    #get user session 
    client_id = session['user']['id']
    #get products from basket
    client = User.get_by_id(client_id)
    pdb.set_trace()
    basket = Basket.get(client_id)
    products = BasketProduct.get_all(client_id)
    return render_template('cart.html',client = client, basket = basket, products = products)



    