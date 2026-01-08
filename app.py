from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Message Model (Database Table)
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create the database table
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/district/<name>")
def district(name):
    return render_template(f"{name}.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Store message in the database
        new_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        return redirect(url_for("thank_you"))  # Redirect to thank-you page

    return render_template("contact.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")  # A separate thank-you page

if __name__ == "__main__":
    app.run(debug=True)
