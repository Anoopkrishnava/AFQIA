from flask import Flask, render_template, request, redirect, url_for, session
import os

from analyzer.impact_analyzer import analyze_database_query
from analyzer.query_analyzer import validate_query
from analyzer.report_generator import generate_report, generate_report_data

app = Flask(__name__)
app.secret_key = "afqia-secret-key"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        old_db = request.files["old_db"]
        new_db = request.files["new_db"]
        query = request.form["query"].strip()

        if not old_db.filename:
            session["form_error"] = "Please select the old database."
            session["entered_query"] = query
            return redirect(url_for("home"))

        if not new_db.filename:
            session["form_error"] = "Please select the new database."
            session["entered_query"] = query
            return redirect(url_for("home"))

        

        old_db_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            old_db.filename
        )

        new_db_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            new_db.filename
        )

        old_db.save(old_db_path)
        new_db.save(new_db_path)

        if query:
            valid_query, query_error = validate_query(
                old_db_path,
                query
            )

            if not valid_query:
                session["form_error"] = "Invalid SQL query. Please check the SQL syntax."
                session["entered_query"] = query
                return redirect(url_for("home"))

        result = analyze_database_query(
            old_db_path,
            new_db_path,
            query
        )

        report_data = generate_report_data(
            result,
            old_db.filename,
            new_db.filename,
            query
        )

        session["report_data"] = report_data


        print(report_data)

        print("Old DB:", old_db.filename)
        print("New DB:", new_db.filename)
        print("Query:", query)

        return redirect(url_for("home"))

    report_data = session.pop("report_data", None)
    form_error = session.pop("form_error", None)
    entered_query = session.pop("entered_query", "")

    return render_template(
        "index.html",
        report_data=report_data,
        form_error=form_error,
        entered_query=entered_query
    )

if __name__ == "__main__":
    app.run(debug=True)