from flask import render_template, request, redirect, url_for
from werkzeug import Response

from app import app
from app.forms import VacanciesSearchForm
from app.get_data import get_vacancies, load_vacancies, get_full_description
from config import main_config


@app.route("/", methods=["GET", "POST"])
def main() -> Response | str:
    form = VacanciesSearchForm()

    if request.method == "POST":
        if form.validate_on_submit():
            negative_text = " ".join(
                [f"NOT {item}" for item in form.negative_text.data.split()]
            )
            text = f"({form.text.data}) {negative_text}"
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
            menu=main_config.main_menu,
        )
    else:
        return render_template(
            template_name_or_list="index.html",
            form=form,
            menu=main_config.main_menu,
        )


@app.route("/vacancies", methods=["GET"])
def vacancies_list() -> str:
    vacancies = load_vacancies()
    return render_template(
        template_name_or_list="vacancies.html",
        vacancies=vacancies,
        menu=main_config.main_menu,
    )


@app.route("/cover_letters", methods=["GET"])
def get_cover_letters() -> str:
    vacancies = load_vacancies()
    vacancies_full_description = get_full_description(vacancies)

    data = "..."

    return render_template(
        template_name_or_list="cover_letters.html",
        data=data,
        menu=main_config.main_menu,
    )
