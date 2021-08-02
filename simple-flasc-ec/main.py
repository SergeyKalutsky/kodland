import bcrypt
from kodland_db import db
from flask import Flask, render_template, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
app = Flask(__name__)


def hashed_password(plain_text_password):
    # Мы добавляем "соль" к нашему пароль, чтобы сделать его декодирование невозможным
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)


app.config.update(
    SECRET_KEY='WOW SUCH SECRET'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(login):
    return User(login)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        item_id = request.form['item_id']
        row = db.cart.get('item_id', item_id)
        if not row:
            data = {'item_id': item_id, 'amount': 1}
            db.cart.put(data)
        else:
            data = {'item_id': item_id, 'amount': row.amount+1}
            db.cart.delete('item_id', item_id)
            db.cart.put(data)

    data = db.items.get_all()
    for row in data:
        res = db.cart.get('item_id', row.id)
        if res:
            row.amount = res.amount
        else:
            row.amount = 0
    return render_template('products.html', data=data)


@app.route('/action')
def action():
    brands = ['Colla', 'Pepppssi', 'Orio', 'Macdak']
    return render_template('action.html',
                           action_name='Весенние скидки',
                           brands=brands)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        # Дополнительная логика
        return redirect(url_for('order'))

    data = db.cart.get_all()
    total_sum = 0
    for row in data:
        item_row = db.items.get('id', row.item_id)
        row.name = item_row.name
        row.description = item_row.description
        row.price = item_row.price
        row.total = row.amount * item_row.price
        total_sum += row.total
    return render_template('cart.html', data=data, total_sum=total_sum)


@app.route("/logout")
def logout():
    logout_user()
    return 'Пока'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        row = db.users.get('login', request.form['login'])
        if not row:
            return render_template('login.html', error='Неправильный логин или пароль')

        if check_password(request.form['password'], row.password):
            user = User(login)  # Создаем пользователя
            login_user(user)  # Логинем пользователя
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Неправильный логин или пароль')
    return render_template('login.html')


@app.route('/contacts')
def contacts():
    return 'Контакты'


def user_data_exists(val):
    row = db.users.get('login', val)
    if row:
        return True
    return False


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        for key in request.form:
            if request.form[key] == '':
                return render_template('register.html', error='Все поля должны быть заполнены!')

        for key in ['login', 'email', 'phone_number']:
            if user_data_exists(request.form[key]):
                return render_template('register.html', error='Пользователь с такими данными уже существует')

        if request.form['password'] != request.form['password_check']:
            return render_template('register.html', error='Пороли не совпадают')
        data = dict(request.form)
        data['password'] = hashed_password(data['password'])
        data.pop('password_check')
        db.users.put(data=data)
        return render_template('register.html', error='Регистрация прошла успешно')
    return render_template('register.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        print(request.form)
    return render_template('order.html')


@app.route('/about')
def about():
    return 'О компании'


if __name__ == "__main__":
    app.run(debug=True)
