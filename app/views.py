from flask import render_template, request, redirect, url_for
from werkzeug import Response

from app import app
from app.forms import VacanciesSearchForm
from app.get_data import get_vacancies, load_vacancies
from config import main_config


@app.route("/", methods=["GET", "POST"])
def main() -> Response | str:
    form = VacanciesSearchForm()
    menu = [
        {"name": "Сначала", "url": "/"},
    ]

    if request.method == "POST":
        if form.validate_on_submit():
            text = f"{form.text.data} {main_config.vac_exception}"
            experience = form.experience.data
            employment = None
            schedule = form.schedule.data

            get_vacancies(
                text=text,
                experience=experience,
                employment=employment,
                schedule=schedule,
            )

            return redirect(url_for("vacancies_list"), 301)

        return render_template(
            template_name_or_list="error.html",
            error=form.errors,
            menu=menu,
        )
    else:
        return render_template(
            template_name_or_list="index.html",
            form=form,
            menu=menu,
        )


@app.route("/vacancies", methods=["GET"])
def vacancies_list() -> str:
    vacancies = load_vacancies()
    menu = [
        {"name": "Новый поиск", "url": "/"},
    ]
    return render_template(
        template_name_or_list="vacancies.html",
        vacancies=vacancies,
        menu=menu,
    )
