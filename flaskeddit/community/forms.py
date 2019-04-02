import re

from flask_wtf import Form
from sqlalchemy import func
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from flaskeddit.models import Community


class CommunityForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Create")

    def validate_name(self, name):
        if re.search(" ", name.data):
            raise ValidationError("Name cannot contain a space.")

        community = Community.query.filter(
            func.lower(Community.name) == name.data.lower()
        ).first()
        if community is not None:
            raise ValidationError("Name is already taken.")
