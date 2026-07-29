from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret123"

# Database connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass123",  
        database="studyplanner"   
    )

# Predefined notes links per subject
notes_links = {
    
    "DBMS":"https://harshrb2424.github.io/Jntuh-R22-Notes/public/?code=DBMS",
    "ATCD":"https://harshrb2424.github.io/Jntuh-R22-Notes/public/?code=ATCD",
    "IAI":"https://harshrb2424.github.io/Jntuh-R22-Notes/public/?code=IAI",
    "JAVA":"https://harshrb2424.github.io/Jntuh-R22-Notes/public/?code=OOPS",
    "DM":"https://harshrb2424.github.io/Jntuh-R22-Notes/public/?code=DM"
}


# Home redirects to login
@app.route("/")
def home():
    return redirect("/login")

# Register
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users(username,password) VALUES(%s,%s)", (username,password))
        db.commit()
        db.close()
        return redirect("/login")
    return render_template("register.html")

# Login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username,password))
        user = cursor.fetchone()
        db.close()

        if user:
            session["user"] = user["id"]
            return redirect("/dashboard")
        else:
            flash("Invalid Email or Password","danger")

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

# Create Study Plan
@app.route("/create_plan", methods=["GET","POST"])
def create_plan():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        subject = request.form["subject"]
        topics = request.form["topics"].split(",")
        exam_date = request.form["exam_date"]

        today = datetime.today()
        exam = datetime.strptime(exam_date,"%Y-%m-%d")
        days = max((exam - today).days, 1)  # avoid zero division

        db = get_db()
        cursor = db.cursor()

        for i, topic in enumerate(topics):
            study_day = today + timedelta(days=i % days)
            cursor.execute(
                """INSERT INTO study_plans
                (user_id,subject,topic,exam_date,study_date)
                VALUES(%s,%s,%s,%s,%s)""",
                (session["user"], subject, topic.strip(), exam_date, study_day.date())
            )

        db.commit()
        db.close()
        return redirect("/view_plan")

    return render_template("create_plan.html")


# Mark topic as completed
@app.route("/complete/<int:id>")
def complete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE study_plans SET completed=1 WHERE id=%s", (id,))
    db.commit()
    db.close()
    return redirect("/view_plan")

# Delete topic
@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM study_plans WHERE id=%s", (id,))
    db.commit()
    db.close()
    return redirect("/view_plan")

# Reschedule dates
@app.route("/reschedule/<int:id>", methods=["GET","POST"])
def reschedule(id):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM study_plans WHERE id=%s", (id,))
    plan = cursor.fetchone()

    if request.method == "POST":
        new_date = request.form["new_date"]

        cursor.execute(
            "UPDATE study_plans SET study_date=%s WHERE id=%s",
            (new_date, id)
        )

        conn.commit()

        return redirect(("/view_plan"))

    return render_template("reschedule.html", plan=plan)

# View Study Plan
@app.route("/view_plan")
def view_plan():
    if "user" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM study_plans WHERE user_id=%s ORDER BY study_date", (session["user"],))
    plans = cursor.fetchall()

    total = len(plans)
    completed = len([p for p in plans if p["completed"] == 1])
    progress = int((completed/total)*100) if total > 0 else 0

    db.close()
    return render_template("view_plan.html", plans=plans, notes_links=notes_links, total=total, completed=completed, progress=progress)

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)