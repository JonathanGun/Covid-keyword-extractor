from flask_wtf import FlaskForm  # type: ignore
from flask_wtf.file import FileAllowed  # type: ignore
from wtforms import SubmitField, TextAreaField, SelectField, MultipleFileField  # type: ignore
from wtforms.validators import DataRequired  # type: ignore


class MyForm(FlaskForm):
    upload_files = MultipleFileField('Article(s)', validators=[FileAllowed(['txt'], 'Text file only!')])
    keyword = TextAreaField('Keywords (comma separated)', validators=[DataRequired()])
    algorithm = SelectField("Algorithm",
                            choices=[
                                ("boyer_moore", "Boyer-Moore"),
                                ("kmp", "KMP"),
                                ("regex", "Regex"),
                            ],
                            default="regex")
    submit = SubmitField('Submit')
