from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "super-secret-key"

users = [
    {"name": "Anna", "age": 17},
    {"name": "Tom", "age": 25},
    {"name": "Kate", "age": 19},
]


def validate_user_input(name, age_text):
    name = name.strip()
    age_text = age_text.strip()

    if name == "" or age_text == "":
        return "Name and age are required", None, None

    if not name.isalpha():
        return "Name must contain only letters.", None, None

    try:
        age = int(age_text)
    except ValueError:
        return "Age must be a valid number.", None, None

    if age < 0 or age > 120:
        return "Age must be between 0 and 120.", None, None

    return None, name, age


def add_user(name, age):
    users.append({"name": name, "age": age})


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        error, name, age = validate_user_input(
            request.form["name"], request.form["age"]
        )

        if error:
            flash(error, "error")
            return redirect(url_for("home"))

        add_user(name, age)
        flash("User added successfully.", "success")
        return redirect(url_for("home"))

    return render_template("index.html", users=users)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
