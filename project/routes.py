from flask import redirect, url_for, render_template, request, flash, abort
from flask_login import login_user, current_user, login_required, logout_user
from project import app, db, bcrypt
from project.models import Business, User
from project.data import test_businesses, test_users
from project.forms import NewBusinessForm, NewUserForm, LoginForm


with app.app_context():
    db.create_all()
    for test_user in test_users:
        hashed_pswd = bcrypt.generate_password_hash('korte07').decode('utf-8')
        user_obj = User(username=test_user['username'], email=test_user['email'], password=hashed_pswd)
        db.session.add(user_obj)
    for test_business in test_businesses:
        business_obj = Business(title=test_business['title'], contact=test_business['contact'],
                                text=test_business['text'], user_id=test_business['user_id'])
        db.session.add(business_obj)
    db.session.commit()


@app.route('/')
@app.route('/home')
def home():
    return render_template('businesses.html')


@app.route('/business/<int:business_id>')
def business(business_id):
    current_business = Business.query.get_or_404(business_id)
    return render_template('business.html', title=current_business.title, business=current_business)


@app.route('/businesses')
def businesses():
    vallalkozasok_db = db.session.execute(db.select(Business)).scalars()
    print(vallalkozasok_db)
    return render_template('businesses.html', businesses=vallalkozasok_db)


@app.route('/businesses/new', methods=['GET', 'POST'])
@login_required
def create():
    form = NewBusinessForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_business = Business(title=form.title.data, owner=current_user,
                                        contact=form.contact.data, text=form.text.data)
            db.session.add(current_business)
            db.session.commit()
            flash('The business has been saved with the given data.', 'success')
            return redirect(url_for('businesses'))
    return render_template('create.html', title='Create a new business', form=form)


@app.route('/business/<int:business_id>/update', methods=['GET', 'POST'])
@login_required
def update_business(business_id):
    current_business = Business.query.get_or_404(business_id)
    if current_business.owner != current_user:
        abort(403)
    form = NewBusinessForm()
    if form.validate_on_submit():
        current_business.title = form.title.data
        current_business.contact = form.contact.data
        current_business.text = form.text.data
        db.session.commit()
        flash('The business has been updated.', 'success')
        return redirect(url_for('business', business_id=current_business.id))
    elif request.method == 'GET':
        form.title.data = current_business.title
        form.contact.data = current_business.contact
        form.text.data = current_business.text
    return render_template('create.html', title='Update business', form=form, legend='Update of the businesses data')


@app.route('/course/<int:business_id>/delete', methods=['POST'])
@login_required
def delete_business(business_id):
    current_business = Business.query.get_or_404(business_id)
    if current_business.owner != current_user:
        abort(403)
    db.session.delete(current_business)
    db.session.commit()
    flash('The business has been deleted.', 'success')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = NewUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration succesful. Log in.', 'success')
        print(User.query.all())
        return redirect(url_for('businesses'))
    return render_template('register.html', title='Create a profile', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('The login attempt was unsuccesful. Please try again.', 'danger')
    return render_template('login.html', title='Log in', form=form)


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Profile')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/message_board')
def message_board():
    return redirect(url_for('home'))
