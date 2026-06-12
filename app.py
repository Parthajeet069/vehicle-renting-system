from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'parth_secret_key'

# DATABASE PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "vehicles.db")

# CREATE DATABASE
conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS rentals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    vehicle_name TEXT,
    days INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT
)
''')

conn.commit()
conn.close()

# SHOP NAME
shop_name = "Parth Vehicle Rentals"

# VEHICLE CATEGORIES
categories = {

    'SUV': [
        {
            'name': 'Mahindra Scorpio N',
            'price': 3999,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiq6ghr8-EMZlpyya1uxvu0C4lorkE-8doEcawfzQXZQ&s=10'
        },

        {
            'name': 'Toyota Fortuner',
            'price': 3999,
            'image': 'https://i.pinimg.com/474x/1a/ff/4f/1aff4fc128198e95669dffffc6269711.jpg'
        },

        {
            'name': 'Ford Endeavour',
            'price': 3999,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuMcJPqoeElpASbUFw2oYz9l-zoBn2aDjnHcagsWZJkOY-2z8hF0m_DNk&s=10'
        },

        {
            'name': 'Mahindra XUV 700',
            'price': 3999,
            'image': 'https://www.carblogindia.com/wp-content/uploads/2022/02/Modified-Mahindra-XUV700-Tank.jpg'
        },

        {
            'name': 'Kia Seltos',
            'price': 3999,
            'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7-0jxEF7du3lC2l9kAJUlEvzLguoOmbxv06qeSGWwkZtfUWbxyDgr2j1F&s=10'
        },

        {
            'name': 'Toyota Hilux',
            'price': 3999,
            'image': 'https://www.team-bhp.com/sites/default/files/pictures2023-09/t2_7.jpeg'
        }
    
    ],

    'Scooty': [
        {
            'name': 'Honda Activa',
            'price': 999,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_9kI1SGRIs7e1SaDT_wRipl4aHa6qSI9vQUergP-gYw&s=10'
        },

        {
            'name': 'TVS Jupiter',
            'price': 999,
            'image': 'https://5.imimg.com/data5/SELLER/Default/2022/9/JE/YG/PI/159878264/tvs-jupiter-jupiter.jpg'
        },

        {
            'name'  : 'Honda Dio',
            'price' : 999,
            'image' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiMQG1X6O9IAkv6hjPfnjvm7qgHrrERqU64vSFNJVCig&s=10'
        },

        {
            'name'  : 'TVS Ntorq',
            'price' : 999,
            'image' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6RVtHvbIjdQ2YSIOu6aNTZ8TcpucxHWeOvlmhq2iIQw&s=10'
        },

        {
            'name'  : 'Yamaha Fascino',
            'price' : 999,
            'image' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQng6K3kk7oJbDdVfqOQ5OMnr3BAf30lR-unXbNqsq20g&s=10'
        }
    ],

    'Bike': [
        {
            'name': 'Royal Enfield Classic 350',
            'price': 1699,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrnX0FxlCh1xlQqDxTyjou-K8RJOfF_UCgH86wTq_GxyTDvvfuFlWiPUs&s=10'
        },

        {
            'name': 'KTM Duke 390',
            'price': 1699,
            'image': 'https://images.91wheels.com/assets/b_images/gallery/ktm/duke-390/ktm-duke-390-0-1768625946.png?w=850&q=40'
        },

        { 
            'name'  : 'Continental GT650',
            'price' : 1699,
            'image' : 'https://media.zigcdn.com/media/content/2023/Apr/cover_64329971e5a76.png' 
        },

        { 
            'name'  : 'Husqvarna Vitpilen' ,
            'price' : 1699,
            'image' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ--aTQFiapOV0GqhMpBDf-HrW781ycpctJk8ojbRhJpQ&s=10' 
        },

        { 
            'name'  : 'Himalayan 450' ,
            'price' : 1699,
            'image' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSclnT_ZhdEtwwVNh8tGtVIpV7KruiTf54pgLiY4A087w&s=10' 
        },

        { 
            'name'  : 'Hero Xpulse' ,
            'price' : 1699,
            'image' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMpDzCp2nS1sqKgXh44hg_t0K-m_7l6Hspx3sFqSQ2SQ&s=10' 
        } 
    ],

    'Sedan': [
        {
            'name': 'Honda City',
            'price': 2999,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZ8Wa1OOSPohELkDOD9Q1sazuGhRDbb5VNnV49eVy5ug&s=10'
        },

        {
            'name': 'Hyundai Verna',
            'price': 2999,
            'image': 'https://carbikeinsight.in/wp-content/uploads/2025/08/WhatsApp-Image-2025-08-23-at-20.57.36_0f8b8a1b-1024x634.jpg'
        },

        {
            'name' :'Skoda Slavia',
            'price' : 2999,
            'image' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTa8kxT_RWYAYbPDfkgCFLsTvhR0gR1GWLgO0OiEpB-l7TxJ9j9ONgFPIwB&s=10'
        },

        {
            'name' : 'Honda Civic',
            'price' : 2999,
            'image' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc92Vbk-KgnySHkGdBts8koos6tfc2SXkA-RX4iSVkqQ&s=10'
        }
    ],

    'Luxury Cars': [
        {
            'name': 'BMW X5',
            'price': 11111,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1fbzpwkLhLlulSZtMC3uKyCzeGZmBxUuRrw7cRjemug&s=10'
        },

        {
            'name': 'Mercedes Benz C-Class',
            'price': 11111,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7ITZ3CCFlrWnRBhlQqZPG1lrElu8daijL296uq29KmQ&s=10'
        },

        {
            'name' : 'Porsche 911',
            'price': 11111,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXABi32ga9__Oou5Kp0JiQRAnNwQ4Sq7i3OP8ekmAdUQ&s=10'
        },

        {
            'name' : 'Toyota Supra',
            'price': 11111,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRH8vshLDggisQh56YR-6OJvgt97oD973aRBSXRoq9tBw&s=10'
        },

        {
            'name' : 'BMW M5 Compi',
            'price': 11111,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8f5Izpav1rjplPikc9JmNf_XsadZ5H_3vGocf0vm2iyQIWsK0zdT9eIln&s=10'
        },

        {
            'name' : 'Ford Mustang',
            'price': 11111,
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbaUdcj9cyMDkNI7d5h7kdkjC-aED3meFKc3I9n9r3ng&s'
        }
    ]
}

# HOME PAGE
@app.route('/')
def home():

    category_names = list(categories.keys())

    first_category = category_names[0]

    return render_template(
    'index.html',
    categories=categories,
    shop_name=shop_name,
    category_names=category_names,
    selected_category=first_category,
    vehicles=categories[first_category],
    username=session.get('user')
)

# CATEGORY PAGE
@app.route('/category/<category_name>')
def category_page(category_name):

    vehicles = categories.get(category_name, [])

    return render_template(
    'category.html',
    selected_category=category_name,
    vehicles=vehicles,
    username=session.get('user')
    )

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # CHECK USER EXISTS

        cursor.execute(
            'SELECT * FROM users WHERE email=?',
            (email,)
        )

        existing_user = cursor.fetchone()

        # EMAIL NOT FOUND

        if not existing_user:

            conn.close()

            return redirect('/signup')

        # CHECK PASSWORD

        cursor.execute(
            'SELECT * FROM users WHERE email=? AND password=?',
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        # LOGIN SUCCESS

        if user:

            session['user'] = user[1]

            return redirect('/')

        else:

            error = "Incorrect Password!"

    return render_template(
        'login.html',
        error=error
    )

# SIGNUP PAGE
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    error = None

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # CHECK USERNAME

        cursor.execute(
            'SELECT * FROM users WHERE username=?',
            (username,)
        )

        existing_username = cursor.fetchone()

        # CHECK EMAIL

        cursor.execute(
            'SELECT * FROM users WHERE email=?',
            (email,)
        )

        existing_email = cursor.fetchone()

        # USERNAME EXISTS

        if existing_username:

            error = "Username already exists!"

        # EMAIL EXISTS

        elif existing_email:

            error = "Email already registered!"

        else:

            # INSERT USER

            cursor.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, password)
            )

            conn.commit()

            session['user'] = username

            conn.close()

            return redirect('/')

        conn.close()

    return render_template(
        'signup.html',
        error=error
    )

# LOGOUT
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')


# RENT PAGE
@app.route('/rent/<vehicle_name>', methods=['GET', 'POST'])
def rent(vehicle_name):

    if 'user' not in session:

        return redirect('/login')

    if request.method == 'POST':

        customer_name = request.form['customer_name']
        days = int(request.form['days'])

        license_number = request.form['license']

        aadhaar_file = request.files['aadhaar']

        # FIND VEHICLE DETAILS

        vehicle_type = ""
        vehicle_price = 0

        for category, vehicle_list in categories.items():

            for vehicle in vehicle_list:

                if vehicle['name'] == vehicle_name:

                    vehicle_type = category
                    vehicle_price = vehicle['price']

        total_amount = vehicle_price * days

        # SAVE TO DATABASE

        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO rentals (customer_name, vehicle_name, days) VALUES (?, ?, ?)',
            (customer_name, vehicle_name, days)
        )

        conn.commit()
        conn.close()

        # SUCCESS PAGE

        return render_template(
            'success.html',
            vehicle_name=vehicle_name,
            vehicle_type=vehicle_type,
            days=days,
            total_amount=total_amount
        )

    return render_template(
        'rent.html',
        vehicle_name=vehicle_name
    )
app.run()