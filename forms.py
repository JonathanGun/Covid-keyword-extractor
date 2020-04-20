from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, MultipleFileField, BooleanField, StringField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    upload_files = MultipleFileField('Article file(s)', render_kw={"placeholder": "You can upload more than one file"})
    text = TextAreaField('Article text', render_kw={"placeholder": "Paste text here"})
    link = StringField('Article link', render_kw={"placeholder": "Paste link here"})
    keyword = TextAreaField('Keywords (comma separated)', validators=[DataRequired()], render_kw={"placeholder": "i.e: PDP,ODP,dalam pengawasan,positif,negatif,sembuh,meninggal"})
    algorithm = SelectField("Algorithm",
                            choices=[
                                ("boyer_moore", "Boyer-Moore"),
                                ("kmp", "KMP"),
                                ("regex", "Regex"),
                            ],
                            default="regex")
    allow_weak = BooleanField('Allow weak/partial match?')
    submit = SubmitField('Submit')
