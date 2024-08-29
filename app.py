from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dog_care.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class DogOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    dogs = db.relationship('Dog', backref='owner', lazy=True)

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('dog_owner.id'), nullable=False)
    eating_time = db.Column(db.String(100), nullable=True)
    food_types = db.Column(db.String(100), nullable=True)
    washroom_time = db.Column(db.String(100), nullable=True)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        user_type = request.form['user_type']
        user = DogOwner.query.filter_by(phone_number=phone_number, user_type=user_type).first()
        if user:
            if user_type == 'caretaker':
                return redirect(url_for('caretaker_dashboard'))
            elif user_type == 'customer':
                return redirect(url_for('customer_dashboard', phone_number=phone_number))
        flash('Invalid login credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        user_type = request.form['user_type']
        new_user = DogOwner(phone_number=phone_number, user_type=user_type)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful, please login.')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Phone number already exists.')
    return render_template('signup.html')

@app.route('/caretaker_dashboard')
def caretaker_dashboard():
    dogs = Dog.query.all()
    return render_template('caretaker_dashboard.html', dogs=dogs)

@app.route('/customer_dashboard/<phone_number>')
def customer_dashboard(phone_number):
    owner = DogOwner.query.filter_by(phone_number=phone_number).first()
    dogs = Dog.query.filter_by(owner_id=owner.id).all()
    return render_template('customer_dashboard.html', dogs=dogs)

@app.route('/add_dog', methods=['POST'])
def add_dog():
    name = request.form['name']
    phone_number = request.form['phone_number'].strip()
    owner = DogOwner.query.filter_by(phone_number=phone_number).first()
    if owner:
        new_dog = Dog(name=name, owner=owner)
        db.session.add(new_dog)
        db.session.commit()
        flash('Dog added successfully.')
    else:
        flash('Owner not found', 'error')
    return redirect(url_for('caretaker_dashboard'))

@app.route('/update_dog/<int:dog_id>', methods=['GET', 'POST'])
def update_dog(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    if request.method == 'POST':
        eating_time = request.form['eating_time']
        food_types = request.form.getlist('food_types')
        washroom_time = request.form['washroom_time']
        
        dog.eating_time = eating_time
        dog.food_types = ', '.join(food_types)
        dog.washroom_time = washroom_time
        
        db.session.commit()
        flash('Dog information updated successfully.')
        return redirect(url_for('caretaker_dashboard'))
    
    return render_template('update_dog.html', dog=dog)

class KennelBoarding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    breed = db.Column(db.String(100), nullable=True)
    vaccination_details = db.Column(db.Text, nullable=True)
    owner_name = db.Column(db.String(100), nullable=False)
    aadhar_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    contact_number = db.Column(db.String(15), nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_number = db.Column(db.String(15), nullable=True)
    vet_clinic_name = db.Column(db.String(100), nullable=True)
    vet_contact_number = db.Column(db.String(15), nullable=True)
    boarding_type = db.Column(db.String(50), nullable=True)
    check_in_date = db.Column(db.Date, nullable=True)
    check_out_date = db.Column(db.Date, nullable=True)
    breakfast = db.Column(db.String(100), nullable=True)
    lunch = db.Column(db.String(100), nullable=True)
    dinner = db.Column(db.String(100), nullable=True)
    other_information = db.Column(db.Text, nullable=True)
    medication_name = db.Column(db.String(100), nullable=True)
    dosage = db.Column(db.String(100), nullable=True)
    administration_instructions = db.Column(db.Text, nullable=True)
    last_heat_cycle_date = db.Column(db.Date, nullable=True)
    temperament = db.Column(db.Integer, nullable=True)
    socializing = db.Column(db.String(100), nullable=True)
    separation_anxiety = db.Column(db.String(100), nullable=True)
    bath_specifications = db.Column(db.Text, nullable=True)
    swimming_specifications = db.Column(db.Text, nullable=True)

@app.route('/boarding_form', methods=['GET', 'POST'])
def submit_boarding_form():
    if request.method == 'POST':
        pet_name = request.form.get('pet_name')
        dob = request.form.get('dob')
        age = request.form.get('age')
        gender = request.form.get('gender')
        breed = request.form.get('breed')
        vaccination_details = request.form.get('vaccination_details')
        owner_name = request.form.get('owner_name')
        aadhar_number = request.form.get('aadhar_number')
        address = request.form.get('address')
        email = request.form.get('email')
        contact_number = request.form.get('contact_number')
        emergency_contact_name = request.form.get('emergency_contact_name')
        emergency_contact_number = request.form.get('emergency_contact_number')
        vet_clinic_name = request.form.get('vet_clinic_name')
        vet_contact_number = request.form.get('vet_contact_number')
        boarding_type = request.form.get('boarding_type')
        check_in_date = request.form.get('check_in_date')
        check_out_date = request.form.get('check_out_date')
        breakfast = request.form.getlist('breakfast')
        lunch = request.form.getlist('lunch')
        dinner = request.form.getlist('dinner')
        other_information = request.form.get('other_information')
        medication_name = request.form.get('medication_name')
        dosage = request.form.get('dosage')
        administration_instructions = request.form.get('administration_instructions')
        last_heat_cycle_date = request.form.get('last_heat_cycle_date')
        temperament = request.form.get('temperament')
        socializing = request.form.get('socializing')
        separation_anxiety = request.form.get('separation_anxiety')
        bath_specifications = request.form.get('bath_specifications')
        swimming_specifications = request.form.get('swimming_specifications')

        # Convert string dates to Python date objects
        dob = datetime.strptime(dob, '%Y-%m-%d').date() if dob else None
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date() if check_in_date else None
        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date() if check_out_date else None
        last_heat_cycle_date = datetime.strptime(last_heat_cycle_date, '%Y-%m-%d').date() if last_heat_cycle_date else None

        new_boarding = KennelBoarding(
            pet_name=pet_name, dob=dob, age=age, gender=gender, breed=breed,
            vaccination_details=vaccination_details, owner_name=owner_name,
            aadhar_number=aadhar_number, address=address, email=email,
            contact_number=contact_number, emergency_contact_name=emergency_contact_name,
            emergency_contact_number=emergency_contact_number, vet_clinic_name=vet_clinic_name,
            vet_contact_number=vet_contact_number, boarding_type=boarding_type,
            check_in_date=check_in_date, check_out_date=check_out_date,
            breakfast=",".join(breakfast), lunch=",".join(lunch), dinner=",".join(dinner),
            other_information=other_information, medication_name=medication_name,
            dosage=dosage, administration_instructions=administration_instructions,
            last_heat_cycle_date=last_heat_cycle_date, temperament=temperament,
            socializing=socializing, separation_anxiety=separation_anxiety,
            bath_specifications=bath_specifications, swimming_specifications=swimming_specifications
        )

        db.session.add(new_boarding)
        db.session.commit()
        flash('Boarding form submitted successfully!', 'success')
        return redirect(url_for('submit_boarding_form'))

    return render_template('boarding_form.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
