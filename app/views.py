from flask import render_template, request, redirect, url_for
from werkzeug import Response

from app import app
from app.forms import VacanciesSearchForm
from app.get_data import (
    get_vacancies,
    load_vacancies,
    get_full_description,
    load_full_vacancies,
)
from app.processing_data import (
    check_skills,
    del_vacancy_by_id,
    generate_all_latter,
    get_data_for_table,
)
from app.utils import (
    send_all_negotiations,
    get_all_negotiations,
    add_row_to_goggle_sheet,
    send_negotiation,
)
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

            vacancies = get_vacancies(
                text=text,
                experience=experience,
                employment=employment,
                schedule=schedule,
            )

            get_full_description(vacancies)

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
    data = load_full_vacancies()
    if "coincidence" not in data[0]:
        check_skills(data)

    vacancies = load_vacancies()

    return render_template(
        template_name_or_list="vacancies.html",
        vacancies=vacancies,
        menu=main_config.main_menu,
    )


@app.route("/cover_letters", methods=["GET"])
def get_cover_letters() -> str:
    data = load_full_vacancies()

    if "cover_letter" not in data[0]:
        generate_all_latter(data)

        data = load_full_vacancies()

    return render_template(
        template_name_or_list="cover_letters.html",
        data=data,
        menu=main_config.main_menu,
    )


@app.route("/vacancies/<vac_id>", methods=["POST"])
def del_vacancy(vac_id: str) -> Response:
    del_vacancy_by_id(vac_id=vac_id)
    return redirect(url_for("vacancies_list"), 301)


@app.route("/cover_letters/send_all", methods=["GET"])
def send_all():
    send_all_negotiations()
    return redirect(url_for("get_cover_letters"), 301)


@app.route("/cover_letters/<vac_id>", methods=["GET"])
def send_negotiation_by_vacancy(vac_id: str):
    send_negotiation(
        vac_id,
    )
    return redirect(url_for("get_cover_letters"), 301)


@app.route("/vacancies/negotiations", methods=["GET"])
def get_negotiations():
    data = get_all_negotiations()
    return render_template(
        template_name_or_list="negotiations.html",
        data=data,
        menu=main_config.main_menu,
    )


@app.route("/cover_letters/add_to_table/<vac_id>", methods=["GET"])
def add_row_in_google_table(vac_id: str):
    data = get_data_for_table(vac_id)
    add_row_to_goggle_sheet(data)
    return redirect(url_for("get_cover_letters"), 301)
