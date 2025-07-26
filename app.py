from flask import Flask, request, render_template, redirect
import mysql.connector
import joblib
import numpy as np

app = Flask(__name__, template_folder='templates', static_folder='static')

# Connect to RDS MySQL
conn = mysql.connector.connect(
    host='agriculture-database.cgni8q8qy7bh.us-east-1.rds.amazonaws.com',
    user='SimranNegi',
    password='agri-web0000',
    database='agriculture'
)
cursor = conn.cursor()

# Load ML model
model = joblib.load("crop_recommendation_model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

# ✅ SIGN UP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['Name']
        email = request.form['Email']
        password = request.form['Password']
        govt_id = request.form['GovtId']

        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (Name, Email, Password, GovtId) VALUES (%s, %s, %s, %s)", 
                        (name, email, password, govt_id))
            conn.commit()
            cur.close()
            return redirect("/croprec")  # ✅ Redirect to crop input page after successful signup
        except mysql.connector.IntegrityError:
            return "Email already registered. Try logging in."
        except Exception as e:
            return f"Signup failed: {e}"

    return render_template("signup.html")

# ✅ LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['Email']
        password = request.form['Password']

        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE Email=%s AND Password=%s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            return redirect("/croprec")
        else:
            return "Invalid login credentials"
    return render_template("login.html")

# ✅ Crop Recommendation Page
@app.route("/croprec", methods=["GET"])
def croprec():
    return render_template("cropRec.html")

# ✅ Predict Endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(features)
        predicted_crop = prediction[0]

        return render_template('result.html', recommendation={
            'name': predicted_crop.title(),
            'summary': f"Based on your inputs, we recommend planting {predicted_crop.title()}."
        })

    except Exception as e:
        return f"Prediction failed: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
