from flask import *
from flask_wtf import FlaskForm
from wtforms import StringField ,SelectField, PasswordField, BooleanField 
from wtforms.validators import DataRequired , Length, Email, EqualTo, ValidationError ,NumberRange
from wtforms.fields.html5 import DateField , IntegerField
from wtforms.widgets import html5
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message 

from flask_login import LoginManager ,UserMixin , current_user , login_user , logout_user, login_required


app = Flask(__name__)
#====================config SQLAlchemy=================
app.config['SECRET_KEY'] = 'f6a6ec1916a64e3294f4bf45bf183f81'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
db = SQLAlchemy(app)
#===================config login manager===============
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login first'
login_manager.login_message_category = 'info'
#===================config mail===============
mail= Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '***********************'
app.config['MAIL_PASSWORD'] = '***********************'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#====================Models=======================#
class Ticket(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	travel_from = db.Column(db.String(60), nullable=False)
	travel_to = db.Column(db.String(60), nullable=False)
	travel_with = db.Column(db.String(60), nullable=False)
	date = db.Column(db.String(60), nullable=False)
	price = db.Column(db.String(60), nullable=False)
	def __repr__(self):
		return f'{self.__class__.__name__}({self.id}, {self.travel_from}, {self.travel_to}, {self.travel_with}, {self.date}, {self.price})'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(30), unique=True, nullable=False)
	booking = db.Column(db.String(60), unique=True, nullable=False)
	alltotall = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f'{self.__class__.__name__}({self.id}, {self.user}, {self.booking}, {self.alltotall})'

class Booking(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column (db.Integer, unique=False, nullable=True)
	ticket_id = db.Column(db.Integer, unique=False, nullable=False)
	adult= db.Column(db.Integer, unique=False, nullable=True)
	student= db.Column(db.Integer, unique=False, nullable=True)
	retired=db.Column(db.Integer, unique=False, nullable=True)
	child=db.Column(db.Integer, unique=False, nullable=True)
	totall = db.Column(db.Float, unique=False, nullable=True)

	def __repr__(self):
		return f'{self.__class__.__name__}({self.id},{self.user_id},{self.ticket_id},{self.adult},{self.student},{self.retired},{self.child},{self.totall})'

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	email = db.Column(db.String(60), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f'{self.__class__.__name__}({self.id}, {self.username}, {self.email})'

class Purchase(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(30), unique=True, nullable=False)
	Booking = db.Column(db.String(60), unique=True, nullable=False)
	alltotall = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f'{self.__class__.__name__}({self.user}, {self.booking}, {self.alltotall})'

#====================Forms=======================#
class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25, message='username must be between 4 and 25 characters')])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='passwords must match')])

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('This username already exists')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email already exists')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')


class UpdateProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25, message='username must be between 4 and 25 characters')])
	email = StringField('Email', validators=[DataRequired(), Email()])

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('This username already exists')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('This email already exists')


class cheack (FlaskForm):
	travel_from = SelectField('travel_from', choices=[('', 'Travel from'),('Oslo', 'oslo'), ('Bodø', 'Bodø'),
									('Drammen', 'Drammen'),('Bergen', 'Bergen'),
									('Gjøvik', 'Gjøvik'),('Porsgrunn', 'Porsgrunn'),
									('Bærum', 'Bærum'),('Fjellhamar', 'Fjellhamar'),
									('Kristiansand', 'Kristiansand'),('Fredrikstad', 'Fredrikstad')],  validators=[DataRequired()] )
	travel_to = SelectField('travel_to', choices=[('', 'Travel to'),('Oslo', 'oslo'), ('Bodø', 'Bodø'),
									('Drammen', 'Drammen'),('Bergen', 'Bergen'),
									('Gjøvik', 'Gjøvik'),('Porsgrunn', 'Porsgrunn'),
									('Bærum', 'Bærum'),('Fjellhamar', 'Fjellhamar'),
									('Kristiansand', 'Kristiansand'),('Fredrikstad', 'Fredrikstad')],  validators=[DataRequired()]) 

	travel_with = SelectField('travel_with', choices=[('', 'travel_with'),('Bus', 'Bus'), ('Train', 'Train')],  validators=[DataRequired()])
	date = DateField('date', validators=[DataRequired()])
class TicketForm(FlaskForm):
	travel_from = SelectField('travel_from',choices=[('', 'Travel from'),('Oslo', 'oslo'), ('Bodø', 'Bodø'),
									('Drammen', 'Drammen'),('Bergen', 'Bergen'),
									('Gjøvik', 'Gjøvik'),('Porsgrunn', 'Porsgrunn'),
									('Bærum', 'Bærum'),('Fjellhamar', 'Fjellhamar'),
									('Kristiansand', 'Kristiansand'),('Fredrikstad', 'Fredrikstad')],  validators=[DataRequired()])
	
	travel_to = SelectField('Travel_to', choices=[('', 'Travel to'),('Oslo', 'oslo'), ('Bodø', 'Bodø'),
									('Drammen', 'Drammen'),('Bergen', 'Bergen'),
									('Gjøvik', 'Gjøvik'),('Porsgrunn', 'Porsgrunn'),
									('Bærum', 'Bærum'),('Fjellhamar', 'Fjellhamar'),
									('Kristiansand', 'Kristiansand'),('Fredrikstad', 'Fredrikstad')],  validators=[DataRequired()])
	
	travel_with = SelectField('travel_with', choices=[('', 'travel_with'),('Bus', 'Bus'), ('Train', 'Train')],  validators=[DataRequired()])
	date = DateField('date', validators=[DataRequired()])
	price = StringField('price', validators=[DataRequired()])

class PassengerForm(FlaskForm):
	adult =IntegerField('adult' ,widget=html5.NumberInput(min = 0, max = 5),render_kw={"placeholder": "1"},  validators=[DataRequired()])
	student = IntegerField('student' ,widget=html5.NumberInput(min = 0, max = 5),render_kw={"placeholder": "0"},  validators=[DataRequired()])
	retired = IntegerField('retired',widget=html5.NumberInput(min = 0, max = 5),render_kw={"placeholder": "0"},  validators=[DataRequired()])
	child = IntegerField('child',widget=html5.NumberInput(min = 0, max = 5),render_kw={"placeholder": "0" },  validators=[DataRequired()])

class CartForm(FlaskForm):
	cart_naumber = StringField('cart_naumber' , validators=[DataRequired()],render_kw={"placeholder": "1111111111111111"})
	cvv = StringField('cvv' , validators=[DataRequired() ],render_kw={"placeholder": "1111"})
	date_mm = StringField('date_mm' , validators=[DataRequired()],render_kw={"placeholder": "01"})
	date_yy = StringField('date_yy' , validators=[DataRequired()],render_kw={"placeholder": "2021"})
#====================Routes=======================#
@app.route("/" , methods=['GET', 'POST'])
def home():
    ticket=""
    form=cheack()
    if form.validate_on_submit():
        ticket = Ticket.query.filter_by(travel_from=form.travel_from.data,travel_to=form.travel_to.data,travel_with=form.travel_with.data,date=form.date.data).all()
    return render_template('index.html', form=form , tickets=ticket )

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and (user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			flash('you logged in successfully', 'success')
			return redirect(next_page if next_page else url_for('home'))
		else:
			flash('Email or Password is wrong', 'danger')
	return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('you registered successfully', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('you logged out successfully', 'success')
	return redirect(url_for('home'))




@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	form = UpdateProfileForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('account updated', 'info')
		return redirect(url_for('profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('profile.html', form=form)


@app.route('/ticket/<int:ticket_id>' ,methods=['GET', 'POST'])
@login_required
def detail(ticket_id):
	user = current_user.id 
	ticket = Ticket.query.get_or_404(ticket_id)
	form=PassengerForm()
	totall=int(ticket.price)
	alltotall=""
	if form.validate_on_submit():
		student=int(form.student.data)
		student=(student/2)  * totall
		adult=int(form.adult.data)
		adult=adult*totall
		retired=int(form.retired.data)
		retired=(retired/2)  * totall
		alltotall = adult+student+retired
		booking = Booking(user_id=current_user.id ,ticket_id=ticket_id,adult=form.adult.data,student=form.student.data,retired=form.retired.data,child=form.child.data,totall=alltotall)
		db.session.add(booking)
		db.session.commit()
		return redirect(url_for('payment'))
	return render_template('detail.html', ticket=ticket,  form=form, alltotall=alltotall , user=user)



@app.route('/payment/' ,methods=['GET', 'POST'])
def payment():
    user = current_user.id
    booking = Booking.query.filter_by(user_id=user).all()[-1]
    sample_cart=('1', '1', '1', '1')
    alltotall= ""
    cart=""
    a = User.query.get_or_404(user)
    form=CartForm()
    if form.validate_on_submit():
    	cart_number = form.cart_naumber.data
    	date_mm= form.date_mm.data
    	date_yy=form.date_yy.data
    	cvv=form.cvv.data
    	cart= (cart_number,date_mm,date_yy,cvv)
    	if cart==sample_cart:
            msg = Message('Ticket', sender = '***********************', recipients = [a.email])
            msg.body = f'thanks for your shopping {a.username} . book a ticket {booking} Successfully registere Issue Tracking {booking.id} '
            mail.send(msg)
            purchase = Purchase(user=user, booking=booking, alltotall=alltotall )
            db.session.add(purchase)
            db.session.commit()
            return "Your purchase is completed successfully"
    return render_template('payment-page.html',form=form, booking=booking )


#=========================admin====================
@app.route('/new', methods=['GET', 'POST'])
def new_ticket():
	form = TicketForm()
	if form.validate_on_submit():
		db.create_all()
		ticket = Ticket(travel_from=form.travel_from.data, travel_to=form.travel_to.data, travel_with=form.travel_with.data, date=form.date.data, price=form.price.data )
		db.session.add(ticket)
		db.session.commit()
		flash('ticket created', 'info')
		return redirect(url_for('home'))
	return render_template('newticket.html', form=form)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,host="0.0.0.0")


