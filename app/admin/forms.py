from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm


class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=1)])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    colors = TextAreaField('Colors', validators=[DataRequired()])
    image_1 = FileField('Image 1 ',
                        validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], message='images only')]
                        )
    image_2 = FileField('Image 2 ',
                        validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], message='images only')]
                        )
    image_3 = FileField('Image 3 ',
                        validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], message='images only')])