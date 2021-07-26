import kodland_db as db
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/contacts')
def contacts():
    return 'Контакты'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
    return render_template('register.html')


@app.route('/about')
def about():
    return 'О компании'


if __name__ == "__main__":
    app.run(debug=True)
