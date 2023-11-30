from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired

from app.get_data import get_dictionaries, dictionaries_to_tuple


class VacanciesSearchForm(FlaskForm):
    choices_dict = dictionaries_to_tuple(get_dictionaries())

    text = StringField(
        label="Название вакансии", default="python", validators=[InputRequired()]
    )
    experience = SelectField(default=None, choices=choices_dict["experience"])
    # employment = SelectField(default=None, choices=choices_dict["employment"])
    schedule = SelectField(default=None, choices=choices_dict["schedule"])
    skills = StringField(label="Основные навыки", default=None)
