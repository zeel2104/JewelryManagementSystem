from flask import Flask
from flask_cors import CORS
from psycopg2 import sql
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message 
from flask import Flask, request, jsonify, url_for
from google.oauth2 import id_token
from google.auth.transport import requests
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
bcrypt = Bcrypt(app) 
CORS(app) 

import psycopg2



# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-password'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'  # Replace with your email

mail = Mail(app)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="jewelry_db",
        user="postgres",
        password="zeel2128"
    )
    return conn


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if user already exists
        cursor.execute("SELECT * FROM customer WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"error": "User already exists"}), 409  # Conflict error

        # Insert new user
        cursor.execute(
            "INSERT INTO customer (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500

    finally:
        cursor.close()
        conn.close()

# # Customer CRUD
# getUser
# updateUser
# deleteUser
# getAllUsers

@app.route('/api/auth/user/<string:name>', methods=['GET'])
def get_user(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT customerid, name, email, role FROM customer WHERE name = %s", (name,))
        user = cursor.fetchone()
        if user:
            return jsonify({"customerid": user[0], "name": user[1], "email": user[2], "role": user[3]}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/auth/user/<string:email>', methods=['PUT'])
def update_user(email):
    data = request.get_json()
    name = data.get('name')
    phoneNumber = data.get('phoneNumber')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE customer SET name = %s, phonenumber = %s WHERE email = %s",
            (name, phoneNumber, email,)
        )
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "User updated successfully"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/user/<string:email>', methods=['DELETE'])
def delete_user(email):
    res, _ = get_user(email)
    data = res.get_json()
    print("Data : " + str(data))
    conn = get_db_connection()
    cursor = conn.cursor()
    customerid = int(data['customerid'])
    try:
        cursor.execute("DELETE FROM customer WHERE customerid = %s", (customerid,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"message": "User deleted successfully"}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT customerid, name, email, phonenumber, purchasehistory, role FROM customer")
        users = cursor.fetchall()
        if users:
            users_list = [
                {"id": user[0], "name": user[1], "email": user[2], "phonenumber": user[3], "purchasehistory": user[4], "role": user[5]} for user in users
            ]
            return jsonify(users_list), 200
        return jsonify({"message": "No users found"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500
    finally:
        cursor.close()
        conn.close()

########################################################

@app.route('/api/auth/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name, password, role FROM customer WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            stored_password = user[1]
            if check_password_hash(stored_password, password):
                return jsonify({
                    "name": user[0],
                    "role": user[2]  # Include the role ('admin' or 'user')
                }), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM customer WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            reset_token = generate_password_hash(email, method='sha256')  # Simulated token
            reset_url = f"http://localhost:4200/reset-password?token={reset_token}"

            # Send email logic here (not implemented for simplicity)
            print(f"Password reset link: {reset_url}")

            return jsonify({"message": "Password reset link sent to your email."}), 200
        else:
            return jsonify({"error": "Email not registered"}), 404
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    new_password = data.get('newPassword')
    email = data.get('email')  # For simplicity, use email. Use token validation in production.

    hashed_password = generate_password_hash(new_password, method='sha256')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE customer SET password = %s WHERE email = %s", (hashed_password, email))
        conn.commit()
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/api/auth/google-signin', methods=['POST'])
def google_signin():
    data = request.get_json()
    token = data.get('token')

    try:
        # Verify the Google ID token with your Google Client ID
        id_info = id_token.verify_oauth2_token(token, requests.Request(), "YOUR_GOOGLE_CLIENT_ID")

        # Extract user information from the ID token
        email = id_info['email']
        name = id_info.get('name', '')  # Optional fields can be handled with defaults

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists in the database
        cursor.execute("SELECT * FROM signup WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            # If the user does not exist, create a new account
            cursor.execute("INSERT INTO signup (email, name) VALUES (%s, %s)", (email, name))
            conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        # Return a success  
        return jsonify({"message": "Google sign-in successful"}), 200

    except ValueError:
        # If the token is invalid
        return jsonify({"error": "Invalid token"}), 400

    except Exception as e:
        # Handle other exceptions
        print("Error:", e)
        return jsonify({"error": "An error occurred during Google sign-in"}), 500





# @app.route('/products', methods=['GET'])
# def get_products():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM products;")
#     products = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return {'products': products}


@app.route('/')
def home():
    return "Hello, Flask is working!"

#********************Product***************


@app.route('/api/products', methods=['GET'])
def get_products():
    products = [
    {
        "ProductID": 1,
        "Name": "Elegant Diamond Ring",
        "Description": "An exquisite diamond ring perfect for engagements and weddings.",
        "CategoryID": 1,
        "Material": "Silver",
        "Price": 5000.00,
        "ImageURL": url_for('static', filename='images/product11.jpg', _external=True)
    },
    {
        "ProductID": 2,
        "Name": "Golden Eternity Band",
        "Description": "Symbolize forever with this stunning eternity band in gold.",
        "CategoryID": 1,
        "Material": "Gold",
        "Price": 5500.00,
        "ImageURL": url_for('static', filename='images/product2.avif', _external=True)
    },
    {
        "ProductID": 3,
        "Name": "Twist Gold Band",
        "Description": "A twisted design ring that reflects elegance and simplicity.",
        "CategoryID": 1,
        "Material": "Gold",
        "Price": 4800.00,
        "ImageURL": url_for('static', filename='images/product3.jpg', _external=True)
    },
    {
        "ProductID": 4,
        "Name": "Pearl Stud Earrings",
        "Description": "Elegant pearl stud earrings to complement any outfit.",
        "CategoryID": 4,
        "Material": "Pearl",
        "Price": 3100.00,
        "ImageURL": url_for('static', filename='images/product4.jfif', _external=True)
    },
    {
        "ProductID": 5,
        "Name": "Classic Leather Strap Watch",
        "Description": "Minimalist leather strap watch for timeless style.",
        "CategoryID": 6,
        "Material": "Leather",
        "Price": 4900.00,
        "ImageURL": url_for('static', filename='images/product5.avif', _external=True)
    },
    {
        "ProductID": 6,
        "Name": "Amethyst Pendant Necklace",
        "Description": "A sparkling amethyst pendant on a sleek silver chain.",
        "CategoryID": 7,
        "Material": "Silver",
        "Price": 8200.00,
        "ImageURL": url_for('static', filename='images/product6.webp', _external=True)
    },
    {
        "ProductID": 7,
        "Name": "Silver Infinity Bracelet",
        "Description": "Delicate bracelet with an infinity charm for a timeless look.",
        "CategoryID": 2,
        "Material": "Silver",
        "Price": 2200.00,
        "ImageURL": url_for('static', filename='images/product7.webp', _external=True)
    },
    {
        "ProductID": 8,
        "Name": "Antique Gold Brooch",
        "Description": "Vintage-style gold brooch with intricate details.",
        "CategoryID": 5,
        "Material": "Gold",
        "Price": 7800.00,
        "ImageURL": url_for('static', filename='images/product8.webp', _external=True)
    },
    {
        "ProductID": 9,
        "Name": "Golden Bell Anklet",
        "Description": "Graceful anklet adorned with tiny gold bells.",
        "CategoryID": 8,
        "Material": "Gold",
        "Price": 1300.00,
        "ImageURL": url_for('static', filename='images/product9.webp', _external=True)
    },
    {
        "ProductID": 10,
        "Name": "Executive Cufflinks Set",
        "Description": "Polished silver cufflinks set for formal and professional attire.",
        "CategoryID": 10,
        "Material": "Silver",
        "Price": 2600.00,
        "ImageURL": url_for('static', filename='images/product10.webp', _external=True)
    },
    {
        "ProductID": 11,
        "Name": "Sapphire Birthstone Necklace",
        "Description": "Personalized necklace featuring a sapphire birthstone.",
        "CategoryID": 1,
        "Material": "Gold",
        "Price": 3600.00,
        "ImageURL": url_for('static', filename='images/product11.jpg', _external=True)
    },
    {
        "ProductID": 12,
        "Name": "Artisan Textured Silver Ring",
        "Description": "Handcrafted silver ring with a unique textured design.",
        "CategoryID": 3,
        "Material": "Silver",
        "Price": 4200.00,
        "ImageURL": url_for('static', filename='images/product12.jpg', _external=True)
    },
    {
        "ProductID": 13,
        "Name": "Golden Hoop Earrings",
        "Description": "Chic and stylish gold hoop earrings for everyday elegance.",
        "CategoryID": 4,
        "Material": "Gold",
        "Price": 2100.00,
        "ImageURL": url_for('static', filename='images/product13.jpg', _external=True)
    },
    {
        "ProductID": 14,
        "Name": "Wedding Jewelry Set",
        "Description": "Complete wedding jewelry set with traditional designs.",
        "CategoryID": 11,
        "Material": "Mixed",
        "Price": 8200.00,
        "ImageURL": url_for('static', filename='images/product14.webp', _external=True)
    },
    {
        "ProductID": 15,
        "Name": "Customized Heart Necklace",
        "Description": "Personalized heart-shaped pendant in gold with a name engraving.",
        "CategoryID": 1,
        "Material": "Gold",
        "Price": 5100.00,
        "ImageURL": url_for('static', filename='images/product15.jpg', _external=True)
    },
    {
        "ProductID": 16,
        "Name": "Fine Silver Chain",
        "Description": "Simple and elegant silver chain perfect for pendants.",
        "CategoryID": 1,
        "Material": "Silver",
        "Price": 1600.00,
        "ImageURL": url_for('static', filename='images/product16.webp', _external=True)
    },
    {
        "ProductID": 17,
        "Name": "Fashion Star Ring",
        "Description": "A bold and shiny ring featuring a star design.",
        "CategoryID": 3,
        "Material": "Mixed",
        "Price": 3100.00,
        "ImageURL": url_for('static', filename='images/product17.jpg', _external=True)
    },
    {
        "ProductID": 18,
        "Name": "Men's Titanium Watch",
        "Description": "Rugged yet sleek titanium watch for all occasions.",
        "CategoryID": 6,
        "Material": "Titanium",
        "Price": 7200.00,
        "ImageURL": url_for('static', filename='images/product18.jpg', _external=True)
    },
    {
        "ProductID": 19,
        "Name": "Children's Butterfly Set",
        "Description": "Adorable jewelry set with butterfly designs for kids.",
        "CategoryID": 11,
        "Material": "Mixed",
        "Price": 1300.00,
        "ImageURL": url_for('static', filename='images/product19.jpg', _external=True)
    },
    {
        "ProductID": 20,
        "Name": "Diamond Solitaire Earrings",
        "Description": "Stunning diamond solitaire earrings for a timeless look.",
        "CategoryID": 4,
        "Material": "Gold",
        "Price": 15500.00,
        "ImageURL": url_for('static', filename='images/product20.jpg', _external=True)
    },
    {
        "ProductID": 21,
        "Name": "Ruby Halo Earrings",
        "Description": "Elegant ruby earrings surrounded by delicate diamonds.",
        "CategoryID": 4,
        "Material": "Gold",
        "Price": 15200.00,
        "ImageURL": url_for('static', filename='images/product21.webp', _external=True)
    },
    {
        "ProductID": 22,
        "Name": "Opal Teardrop Pendant",
        "Description": "A shimmering opal teardrop pendant on a silver chain.",
        "CategoryID": 7,
        "Material": "Silver",
        "Price": 8500.00,
        "ImageURL": url_for('static', filename='images/product22.webp', _external=True)
    },
    {
        "ProductID": 23,
        "Name": "Pearl Choker Necklace",
        "Description": "A sophisticated choker necklace featuring fine pearls.",
        "CategoryID": 1,
        "Material": "Pearl",
        "Price": 12000.00,
        "ImageURL": url_for('static', filename='images/product23.webp', _external=True)
    },
    {
        "ProductID": 24,
        "Name": "Rose Gold Bangle",
        "Description": "Trendy rose gold bangle with delicate engravings.",
        "CategoryID": 2,
        "Material": "Rose Gold",
        "Price": 4500.00,
        "ImageURL": url_for('static', filename='images/product24.jpg', _external=True)
    },
    {
        "ProductID": 25,
        "Name": "Steel Minimalist Pendant",
        "Description": "Modern pendant in stainless steel for a sleek look.",
        "CategoryID": 7,
        "Material": "Stainless Steel",
        "Price": 2100.00,
        "ImageURL": url_for('static', filename='images/product25.png', _external=True)
    },
    {
        "ProductID": 26,
        "Name": "Diamond Tennis Bracelet",
        "Description": "A classic tennis bracelet with dazzling diamonds.",
        "CategoryID": 2,
        "Material": "Platinum",
        "Price": 25000.00,
        "ImageURL": url_for('static', filename='images/product26.jpeg', _external=True)
    },
    {
        "ProductID": 27,
        "Name": "Quartz Analog Watch",
        "Description": "Analog watch with quartz movement and leather strap.",
        "CategoryID": 6,
        "Material": "Leather",
        "Price": 3800.00,
        "ImageURL": url_for('static', filename='images/product27.jpg', _external=True)
    },
    {
        "ProductID": 28,
        "Name": "Men's Signet Ring",
        "Description": "Bold signet ring for a sophisticated and masculine touch.",
        "CategoryID": 3,
        "Material": "Gold",
        "Price": 9400.00,
        "ImageURL": url_for('static', filename='images/product28.jpg', _external=True)
    },
    {
        "ProductID": 29,
        "Name": "Platinum Infinity Necklace",
        "Description": "Platinum necklace featuring an elegant infinity charm.",
        "CategoryID": 1,
        "Material": "Platinum",
        "Price": 18000.00,
        "ImageURL": url_for('static', filename='images/product29.webp', _external=True)
    },
    {
        "ProductID": 30,
        "Name": "Wedding Ring Set",
        "Description": "Matching wedding rings in gold and platinum for couples.",
        "CategoryID": 11,
        "Material": "Mixed",
        "Price": 19000.00,
        "ImageURL": url_for('static', filename='images/product30.webp', _external=True)
    }
]

    search = request.args.get('search', '').lower()
    category = request.args.get('category', '').lower()
    material = request.args.get('material', '').lower()
    min_price = request.args.get('minPrice', type=float, default=None)
    max_price = request.args.get('maxPrice', type=float, default=None)
    sort_by = request.args.get('sortBy', 'newest')

    
    # print(f"Received min_price: {min_price}, max_price: {max_price}")

    # Filter by search term
    if search:
        products = [p for p in products if search in p["Name"].lower() or search in p["Description"].lower()]

    # Filter by category
    if category:
        products = [p for p in products if p["CategoryID"] == int(category)]

    # Filter by material
    if material:
        products = [p for p in products if material in p["Material"].lower()]

    # Filter by price range
    if min_price is not None:
        products = [p for p in products if p["Price"] >= min_price]
    if max_price is not None:
        products = [p for p in products if p["Price"] <= max_price]
    
    print("Minprince : ", min_price)

     

    # Sort products
    if sort_by == 'priceAsc':
        products = sorted(products, key=lambda p: p["Price"])
    elif sort_by == 'priceDesc':
        products = sorted(products, key=lambda p: p["Price"], reverse=True)
    # No sorting necessary for "newest" as we simulate default order by the hardcoded list

    return jsonify(products)
def get_all_products():
    return [
        # Same product list as in /api/products
        {
        "ProductID": 1,
        "Name": "Elegant Diamond Ring",
        "Description": "An exquisite diamond ring perfect for engagements and weddings.",
        "CategoryID": 1,
        "Material": "Silver",
        "Price": 5000.00,
        "ImageURL": url_for('static', filename='images/product11.jpg', _external=True)
    },
    {
        "ProductID": 2,
        "Name": "Golden Eternity Band",
        "Description": "Symbolize forever with this stunning eternity band in gold.",
        "CategoryID": 1,
        "Material": "Gold",
        "Price": 5500.00,
        "ImageURL": url_for('static', filename='images/product2.avif', _external=True)
    },
    {
        "ProductID": 3,
        "Name": "Twist Gold Band",
        "Description": "A twisted design ring that reflects elegance and simplicity.",
        "CategoryID": 1,
        "Material": "Gold",
        "Price": 4800.00,
        "ImageURL": url_for('static', filename='images/product3.jpg', _external=True)
    },
    {
        "ProductID": 4,
        "Name": "Pearl Stud Earrings",
        "Description": "Elegant pearl stud earrings to complement any outfit.",
        "CategoryID": 4,
        "Material": "Pearl",
        "Price": 3100.00,
        "ImageURL": url_for('static', filename='images/product4.jfif', _external=True)
    },
    {
        "ProductID": 5,
        "Name": "Classic Leather Strap Watch",
        "Description": "Minimalist leather strap watch for timeless style.",
        "CategoryID": 6,
        "Material": "Leather",
        "Price": 4900.00,
        "ImageURL": url_for('static', filename='images/product5.avif', _external=True)
    },
    {
        "ProductID": 6,
        "Name": "Amethyst Pendant Necklace",
        "Description": "A sparkling amethyst pendant on a sleek silver chain.",
        "CategoryID": 7,
        "Material": "Silver",
        "Price": 8200.00,
        "ImageURL": url_for('static', filename='images/product6.webp', _external=True)
    },
    {
        "ProductID": 7,
        "Name": "Silver Infinity Bracelet",
        "Description": "Delicate bracelet with an infinity charm for a timeless look.",
        "CategoryID": 2,
        "Material": "Silver",
        "Price": 2200.00,
        "ImageURL": url_for('static', filename='images/product7.webp', _external=True)
    },
    {
        "ProductID": 8,
        "Name": "Antique Gold Brooch",
        "Description": "Vintage-style gold brooch with intricate details.",
        "CategoryID": 5,
        "Material": "Gold",
        "Price": 7800.00,
        "ImageURL": url_for('static', filename='images/product8.webp', _external=True)
    },
    {
        "ProductID": 9,
        "Name": "Golden Bell Anklet",
        "Description": "Graceful anklet adorned with tiny gold bells.",
        "CategoryID": 8,
        "Material": "Gold",
        "Price": 1300.00,
        "ImageURL": url_for('static', filename='images/product9.webp', _external=True)
    },
    {
        "ProductID": 10,
        "Name": "Executive Cufflinks Set",
        "Description": "Polished silver cufflinks set for formal and professional attire.",
        "CategoryID": 10,
        "Material": "Silver",
        "Price": 2600.00,
        "ImageURL": url_for('static', filename='images/product10.webp', _external=True)
    },
    {
        "ProductID": 11,
        "Name": "Sapphire Birthstone Necklace",
        "Description": "Personalized necklace featuring a sapphire birthstone.",
        "CategoryID": 1,
        "Material": "Gold",
        "Price": 3600.00,
        "ImageURL": url_for('static', filename='images/product11.jpg', _external=True)
    },
    {
        "ProductID": 12,
        "Name": "Artisan Textured Silver Ring",
        "Description": "Handcrafted silver ring with a unique textured design.",
        "CategoryID": 3,
        "Material": "Silver",
        "Price": 4200.00,
        "ImageURL": url_for('static', filename='images/product12.jpg', _external=True)
    },
    {
        "ProductID": 13,
        "Name": "Golden Hoop Earrings",
        "Description": "Chic and stylish gold hoop earrings for everyday elegance.",
        "CategoryID": 4,
        "Material": "Gold",
        "Price": 2100.00,
        "ImageURL": url_for('static', filename='images/product13.jpg', _external=True)
    },
    {
        "ProductID": 14,
        "Name": "Wedding Jewelry Set",
        "Description": "Complete wedding jewelry set with traditional designs.",
        "CategoryID": 11,
        "Material": "Mixed",
        "Price": 8200.00,
        "ImageURL": url_for('static', filename='images/product14.webp', _external=True)
    },
    {
        "ProductID": 15,
        "Name": "Customized Heart Necklace",
        "Description": "Personalized heart-shaped pendant in gold with a name engraving.",
        "CategoryID": 1,
        "Material": "Gold",
        "Price": 5100.00,
        "ImageURL": url_for('static', filename='images/product15.jpg', _external=True)
    },
    {
        "ProductID": 16,
        "Name": "Fine Silver Chain",
        "Description": "Simple and elegant silver chain perfect for pendants.",
        "CategoryID": 1,
        "Material": "Silver",
        "Price": 1600.00,
        "ImageURL": url_for('static', filename='images/product16.webp', _external=True)
    },
    {
        "ProductID": 17,
        "Name": "Fashion Star Ring",
        "Description": "A bold and shiny ring featuring a star design.",
        "CategoryID": 3,
        "Material": "Mixed",
        "Price": 3100.00,
        "ImageURL": url_for('static', filename='images/product17.jpg', _external=True)
    },
    {
        "ProductID": 18,
        "Name": "Men's Titanium Watch",
        "Description": "Rugged yet sleek titanium watch for all occasions.",
        "CategoryID": 6,
        "Material": "Titanium",
        "Price": 7200.00,
        "ImageURL": url_for('static', filename='images/product18.jpg', _external=True)
    },
    {
        "ProductID": 19,
        "Name": "Children's Butterfly Set",
        "Description": "Adorable jewelry set with butterfly designs for kids.",
        "CategoryID": 11,
        "Material": "Mixed",
        "Price": 1300.00,
        "ImageURL": url_for('static', filename='images/product19.jpg', _external=True)
    },
    {
        "ProductID": 20,
        "Name": "Diamond Solitaire Earrings",
        "Description": "Stunning diamond solitaire earrings for a timeless look.",
        "CategoryID": 4,
        "Material": "Gold",
        "Price": 15500.00,
        "ImageURL": url_for('static', filename='images/product20.jpg', _external=True)
    },
    {
        "ProductID": 21,
        "Name": "Ruby Halo Earrings",
        "Description": "Elegant ruby earrings surrounded by delicate diamonds.",
        "CategoryID": 4,
        "Material": "Gold",
        "Price": 15200.00,
        "ImageURL": url_for('static', filename='images/product21.webp', _external=True)
    },
    {
        "ProductID": 22,
        "Name": "Opal Teardrop Pendant",
        "Description": "A shimmering opal teardrop pendant on a silver chain.",
        "CategoryID": 7,
        "Material": "Silver",
        "Price": 8500.00,
        "ImageURL": url_for('static', filename='images/product22.webp', _external=True)
    },
    {
        "ProductID": 23,
        "Name": "Pearl Choker Necklace",
        "Description": "A sophisticated choker necklace featuring fine pearls.",
        "CategoryID": 1,
        "Material": "Pearl",
        "Price": 12000.00,
        "ImageURL": url_for('static', filename='images/product23.webp', _external=True)
    },
    {
        "ProductID": 24,
        "Name": "Rose Gold Bangle",
        "Description": "Trendy rose gold bangle with delicate engravings.",
        "CategoryID": 2,
        "Material": "Rose Gold",
        "Price": 4500.00,
        "ImageURL": url_for('static', filename='images/product24.jpg', _external=True)
    },
    {
        "ProductID": 25,
        "Name": "Steel Minimalist Pendant",
        "Description": "Modern pendant in stainless steel for a sleek look.",
        "CategoryID": 7,
        "Material": "Stainless Steel",
        "Price": 2100.00,
        "ImageURL": url_for('static', filename='images/product25.png', _external=True)
    },
    {
        "ProductID": 26,
        "Name": "Diamond Tennis Bracelet",
        "Description": "A classic tennis bracelet with dazzling diamonds.",
        "CategoryID": 2,
        "Material": "Platinum",
        "Price": 25000.00,
        "ImageURL": url_for('static', filename='images/product26.jpeg', _external=True)
    },
    {
        "ProductID": 27,
        "Name": "Quartz Analog Watch",
        "Description": "Analog watch with quartz movement and leather strap.",
        "CategoryID": 6,
        "Material": "Leather",
        "Price": 3800.00,
        "ImageURL": url_for('static', filename='images/product27.jpg', _external=True)
    },
    {
        "ProductID": 28,
        "Name": "Men's Signet Ring",
        "Description": "Bold signet ring for a sophisticated and masculine touch.",
        "CategoryID": 3,
        "Material": "Gold",
        "Price": 9400.00,
        "ImageURL": url_for('static', filename='images/product28.jpg', _external=True)
    },
    {
        "ProductID": 29,
        "Name": "Platinum Infinity Necklace",
        "Description": "Platinum necklace featuring an elegant infinity charm.",
        "CategoryID": 1,
        "Material": "Platinum",
        "Price": 18000.00,
        "ImageURL": url_for('static', filename='images/product29.webp', _external=True)
    },
    {
        "ProductID": 30,
        "Name": "Wedding Ring Set",
        "Description": "Matching wedding rings in gold and platinum for couples.",
        "CategoryID": 11,
        "Material": "Mixed",
        "Price": 19000.00,
        "ImageURL": url_for('static', filename='images/product30.webp', _external=True)
    }
        # Add the rest of the products here
    ]

cart= []
@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    global cart
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)  # Default to 1 if no quantity is provided

    # Check if product already exists in cart
    existing_item = next((item for item in cart if item["ProductID"] == product_id), None)
    if existing_item:
        existing_item["Quantity"] += quantity  # Update quantity if item exists
    else:
        # Add new item to cart if it doesn't exist
        cart.append({"ProductID": product_id, "Quantity": quantity})

    # Return updated cart items
    return jsonify({"message": "Product added to cart", "cart": cart}), 200

# @app.route('/api/cart/add', methods=['POST'])
# def add_to_cart():
#     global cart
    
#     data = request.json
#     print("Received data for add to cart:", data)
#     product_id = data.get("product_id")
#     quantity = data.get("quantity", 1)

#     # Check if product already exists in cart; if so, update quantity
#     existing_item = next((item for item in cart if item["ProductID"] == product_id), None)
#     if existing_item:
#         existing_item["Quantity"] += quantity
#     else:
#         # Add new item to cart
#         cart.append({"ProductID": product_id, "Quantity": quantity})

#     # Get all product details
#     products = get_all_products()  # Function to fetch all products (this should be defined elsewhere in your code)
#     cart_details = []

#     # Retrieve product details and add them to the cart
#     for item in cart:
#         product = next((p for p in products if p["ProductID"] == item["ProductID"]), None)
#         if product:
#             product_with_quantity = {**product, "Quantity": item["Quantity"]}
#             cart_details.append(product_with_quantity)
#     print("Updated cart:", cart) 

#     return jsonify({"message": "Product added to cart", "cart": cart_details}), 200

@app.route('/api/cart/items', methods=['GET'])
def get_cart_items():
    # Mock function to return cart items (assuming you have a product list and cart items)
    cart_details = []
    products = get_all_products()  # Fetch product details
    
    for item in cart:
        product = next((p for p in products if p["ProductID"] == item["ProductID"]), None)
        if product:
            product_with_quantity = {**product, "Quantity": item["Quantity"]}
            cart_details.append(product_with_quantity)

    return jsonify(cart_details)  # Return cart details with quantities and prices


@app.route('/api/cart/update', methods=['PUT'])
def update_cart_item():
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    for item in cart:
        if item["ProductID"] == product_id:
            item["Quantity"] = quantity
            return jsonify({"message": "Cart item updated"}), 200

    return jsonify({"error": "Product not found in cart"}), 404

@app.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
def remove_cart_item(product_id):
    global cart
    cart = [item for item in cart if item["ProductID"] != product_id]
    return jsonify({"message": "Item removed from cart"}), 200

@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    global cart
    cart = []  # Clear the cart
    return jsonify({"message": "Checkout successful"}), 200


# Get all categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CategoryID, Name, Description FROM Category;")
    categories = cursor.fetchall()
    conn.close()
    # Format the response as a list of dictionaries
    categories_list = [
        {"CategoryID": row[0], "Name": row[1], "Description": row[2]} for row in categories
    ]
    return jsonify(categories_list)

# Get a category by ID
@app.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CategoryID, Name, Description FROM Category WHERE CategoryID = %s;", (category_id,))
    category = cursor.fetchone()
    conn.close()
    if category:
        category_data = {"CategoryID": category[0], "Name": category[1], "Description": category[2]}
        return jsonify(category_data)
    else:
        return jsonify({"error": "Category not found"}), 404

# Add a new category
@app.route('/api/categories', methods=['POST'])
def add_category():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Category (Name, Description) VALUES (%s, %s) RETURNING CategoryID;",
                   (data['Name'], data['Description']))
    category_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({"CategoryID": category_id, "Name": data['Name'], "Description": data['Description']}), 201

# Update a category
@app.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Category SET Name = %s, Description = %s WHERE CategoryID = %s RETURNING CategoryID;",
                   (data['Name'], data['Description'], category_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Category updated"}), 200

# Delete a category
@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Category WHERE CategoryID = %s RETURNING CategoryID;", (category_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Category deleted"}), 200


# Contact Us endpoint
@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Log the message data (you could also save it to a database)
    print(f"Received message from {name} ({email}): {message}")

    # Send a confirmation email
    try:
        msg = Message("Contact Us Form Submission",
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        return jsonify({"message": "Your message has been sent successfully."}), 200
    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"error": "Failed to send message"}), 500
    

# Sample FAQ data
faqs = [
    {"question": "How can I track my jewelry order?", "answer": "You can track your order through the order tracking section on your profile page."},
    {"question": "What is the return policy?", "answer": "Our return policy allows returns within 30 days of purchase with a receipt."},
    # Add more FAQs as needed
]

# Endpoint to get FAQs
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    return jsonify(faqs)


# Endpoint to handle support inquiries (for live chat or support messages)
@app.route('/api/support', methods=['POST'])
def handle_support():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # Here you would typically save this to a database or send an email notification
    # For now, we just print it to the console
    print(f"Support inquiry from {name} ({email}): {message}")

    return jsonify({"message": "Support inquiry received. We will get back to you shortly."}), 201



if __name__ == '__main__':
    app.run(debug=True)
















