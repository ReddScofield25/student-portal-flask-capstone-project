from flask import (
    Flask, render_template, request, redirect, url_for, jsonify, abort, flash
)
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from email_validator import validate_email, EmailNotValidError
import json
import os

load_dotenv()   # Load dotenv to use os.getenv

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
DATA_FILE = os.path.join(BASE_DIR, "static", "data", "states-lgas.json")
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_STATUSES = {"admitted", "undecided", "rejected"}

# Configure MySQL credentials in a secure way using os.getenv
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = os.getenv('SECRET_KEY')

mysql = MySQL(app)

# ── Read the bundled states + LGAs data ──────────────
def load_states_data():
    """Returns [{"state": "Abia State", "local": ["Aba North", ...]}, ...]."""
    with open(DATA_FILE, encoding="utf-8") as fh:
        return json.load(fh)


# ════════════════════════════════════════════════════════════════════
# Pages
# ════════════════════════════════════════════════════════════════════

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Portal Forms Page
@app.route("/portal")
def portal():
    return render_template("portal_form.html")

# Form Submission Handler
@app.route("/save_student", methods=["POST"])
def save_student():
    # The submitted fields are read here so you can see their names.
    student = {
        "firstname":  request.form.get("firstname", "").strip(),
        "middlename": request.form.get("middlename", "").strip(), #
        "lastname":   request.form.get("lastname", "").strip(),
        "email":      request.form.get("email", "").strip(),
        "dob":        request.form.get("dob", "").strip(),
        "gender":     request.form.get("gender", "").strip(),
        "phone":      request.form.get("phone", "").strip(),
        "address":    request.form.get("address", "").strip(),
        "state":      request.form.get("state", "").strip(),
        "lga":        request.form.get("lga", "").strip(),
        "nextofkin":  request.form.get("nextofkin", "").strip(),
        "jamb":       request.form.get("jamb", "").strip(),
        "status":     "undecided",           # every new student starts undecided
    }

    # Validate the uploaded image and sanitize its filename
    image = request.files.get("image")
    student["image"] = filename = None
    if image and image.filename:
        filename = secure_filename(image.filename)
        student["image"] = filename
        image.save(os.path.join(UPLOAD_FOLDER, filename))

    #   Check the email looks valid
    if email := student["email"]:
        try:
            validate_email(email)
        except EmailNotValidError as e:
            flash(str(e))
            return render_template("portal_form.html", form_data=request.form)
    
    #   Make sure jamb is a number in range
    if not student["jamb"].isdigit() or not (100 <= int(student["jamb"]) <= 400):
        flash("JAMB score must be a number between 100 and 400.")
        return render_template("portal_form.html", form_data=request.form)

    #   Reject empty required fields. If anything is wrong, re-render the form
    #   with an error message instead of saving.
    error = []
    for detail in student:
        if student[detail] == "":
            if detail != 'middlename':
                error.append(detail)

    if not error:
        conn = mysql.connection
        cur = conn.cursor()
        query = "INSERT INTO details(image, firstname, middlename, lastname, email, dob, gender, phone, address, state, lga, \
        nextofkin, jamb) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            student['image'],
            student['firstname'],
            student['middlename'],
            student['lastname'],
            student['email'],
            student['dob'],
            student['gender'],
            student['phone'],
            student['address'],
            student['state'],
            student['lga'],
            student['nextofkin'],
            student['jamb']
        )
        cur.execute(query, values)
        conn.commit()
        cur.close()
    else:
        flash(f"Enter all required fields: {error[:]}")
        return render_template("portal_form.html", form_data=request.form)

    return redirect(url_for("students"))

# Students List Page
@app.route("/students")
def students():
    # These filters arrive in the query string; any of them may be blank.
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()
    gender = request.args.get("gender", "").strip()
    jamb   = request.args.get("jamb", "").strip()

    #   Each row needs: id, firstname, middlename, lastname, gender, jamb, status.
    if not (search or status or gender or jamb):
        # No filters → return all students.
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("SELECT id, firstname, middlename, lastname, gender, jamb, status FROM details")
        student_list = cur.fetchall()
        cur.close()
    else:
        #   Return all students, applying whichever filters are non-empty:
        #     • search  → name contains this text
        #     • status  → exact match
        #     • gender  → exact match
        #     • jamb    → exact match
        query = '''SELECT id, firstname, middlename, lastname, gender, jamb, status FROM details
        WHERE %s IN (firstname, middlename, lastname) OR status = %s OR gender = %s OR jamb = %s'''

        values = (f"{search}", f"{status}", f"{gender}", f"{jamb}")

        conn = mysql.connection
        cur = conn.cursor()
        cur.execute(query, values)
        student_list = cur.fetchall()
        cur.close()

    return render_template("students.html", students=student_list)

# Student Details Page
@app.route("/student/<int:id>")
def student_detail(id):
    #   FETCH ONE STUDENT BY id FROM YOUR DATABASE
    #   It needs: id, image, firstname, middlename, lastname, email, gender,
    #   phone, dob, address, state (or state_name), lga (or lga_name),
    #   nextofkin, jamb, status.
    student = None             # ← replace with the row for this id

    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM details WHERE id = %s", (id,))
    student = cur.fetchone()
    cur.close()

    if student is None:
        abort(404)             # no such student yet
    return render_template("student_details.html", student=student)

# Student Status Update Page
@app.route("/update_status", methods=["POST"])
def update_status():
    # status.js sends JSON; this also accepts a normal form post.
    payload = request.get_json(silent=True) or request.form
    student_id = payload.get("student_id")
    new_status = payload.get("status")

    # Reject anything that isn't one of the three allowed values.
    if new_status not in ALLOWED_STATUSES:
        return jsonify(error=f"Invalid status '{new_status}'."), 400

    # UPDATE THIS STUDENT'S STATUS IN YOUR DATABASE (by student_id)
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("UPDATE details SET status = %s WHERE id = %s", (new_status, student_id))
    conn.commit()
    cur.close()

    return jsonify(success=True, status=new_status)


# ════════════════════════════════════════════════════════════════════
# Async data endpoints (feed static/js/locations.js)
# Provided working so the form's dropdowns function once you write the
# fetch() calls. If you'd rather store states/LGAs in your own database,
# replace the bodies below with DB queries.
# ════════════════════════════════════════════════════════════════════

@app.route("/api/states")
def api_states():
    data = load_states_data()
    return jsonify([row["state"] for row in data])


@app.route("/api/lgas/<state>")
def api_lgas(state):
    for row in load_states_data():
        if row["state"] == state:
            return jsonify(row["local"])
    return jsonify([])          # unknown state → empty list


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)