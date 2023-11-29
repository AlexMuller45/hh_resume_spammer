from flask import render_template

from app import app
from app.forms import VacanciesSearchForm


@app.route("/", methods=["GET", "POST"])
def main():
    form = VacanciesSearchForm()

    return render_template("index.html", form=form)
