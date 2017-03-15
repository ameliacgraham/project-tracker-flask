from flask import Flask, request, render_template, url_for, redirect

import hackbright

app = Flask(__name__)

# extracts information from search form
@app.route("/student-find")
def find_student():
    """Processes search form."""
    github = request.args.get('github')
    # redirects user to get_student function passing in github as parameter
    return redirect(url_for("get_student", github=github))


# call get_student_by_github method, extract info from database and renders it
@app.route("/student/<github>")
def get_student(github):
    """Show information about a student."""

    first, last, github = hackbright.get_student_by_github(github)
    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github)

# renders search form
@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

# renders add form
@app.route("/student-add")
def get_student_add_form():
    """Add a student."""

    return render_template("student_add.html")

# receives add form via post method, extracts form information 
# and calls method to create new student in database, then 
# redirects to student/github route, passing in github as parameter
@app.route("/student-created", methods=['POST'])
def get_student_created():
    """Add a student."""


    github = request.form.get("github")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")

    hackbright.make_new_student(first_name, last_name, github)

    return redirect(url_for("get_student", github=github))

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
