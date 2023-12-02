from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired

from app.get_data import get_dictionaries, dictionaries_to_tuple


vac_exception: str = (
    "JAVA "
    "JavaScript "
    "TypeScript "
    "1C "
    "аналитик "
    "Frontend "
    "Data "
    "ML "
    "Преподаватель "
    "поддержки"
)

vac_default: str = "python OR ( python (junior OR разработчик OR backend OR developer))"


class VacanciesSearchForm(FlaskForm):
    choices_dict = dictionaries_to_tuple(get_dictionaries())

    text = StringField(
        label="Название вакансии", default=vac_default, validators=[InputRequired()]
    )
    negative_text = StringField(label="Исключить из поиска", default=vac_exception)
    experience = SelectField(default=None, choices=choices_dict["experience"])
    # employment = SelectField(default=None, choices=choices_dict["employment"])
    schedule = SelectField(default=None, choices=choices_dict["schedule"])
    skills = StringField(label="Основные навыки", default=None)
