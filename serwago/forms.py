from cProfile import label
from secrets import choice
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, FieldList, Form, FormField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp
from serwago.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('E-mail Address already exists! Please try a different email address')

    username = StringField(label="Username", validators=[Length(min=2, max=30, message="The username is too short or too long. Use 2-30 characters."), DataRequired(), Regexp(r'^[\w.@+-]+$', message="Use correct characters:[0-9],[a-z], special characters")])
    email_address = StringField(label=" E-mail address:", validators=[Email(message="E-mail is not in a correct format. Use a correct e-mail address."),DataRequired()])
    password1 = PasswordField(label = "Password", validators=[Length(min=8, max=15, message="The password is too short. Use at least 8 characters"),DataRequired(), Regexp(r'^[\w.@+-]+$', message="Use correct characters:[0-9],[a-z], special characters")])
    password2 = PasswordField(label = "Confirm Password", validators=[EqualTo("password1","The passwords don't match"),DataRequired(), Regexp(r'^[\w.@+-]+$', message="Use correct characters:[0-9],[a-z], special characters")], )
    submit = SubmitField(label = "Create Account")

class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired(), Length(min=2, max=30), Regexp(r'^[\w.@+-]+$')])
    password = PasswordField(label='Password:', validators=[DataRequired(), Length(min=8,max=15), Regexp(r'^[\w.@+-]+$')])
    submit = SubmitField(label='Sign in')

class ProfileForm(FlaskForm):
    first_name = StringField(label="First name", validators=[DataRequired()])
    last_name = StringField(label="Last name", validators=[DataRequired()])
    gender = StringField(label="Gender", validators=[DataRequired()])
    nationality = StringField(label="Nationality", validators=[DataRequired()])
    phone_number = IntegerField(label="Phone", validators=[DataRequired()])
    street_number = IntegerField(label="Phone", validators=[DataRequired()])
    street_name = StringField(label="Nationality", validators=[DataRequired()])
    zip_code = IntegerField(label="Nationality", validators=[DataRequired()])
    submit = SubmitField(label = "Save Profile")

class ProductForm(Form):
    name = StringField(label="Name", validators=[DataRequired()])
    qty = IntegerField(label="Quantity", validators=[DataRequired()])
    total = IntegerField(label="Total", validators=[DataRequired()])
    price = FloatField(label="Price", validators=[DataRequired()])

class CartForm(FlaskForm):
    products = FieldList(FormField(ProductForm), label="Products", min_entries=0, max_entries=999)
    amount = FloatField(label="Amount", validators=[DataRequired()])
    coupon_code = StringField(label="Coupon code")
    note_msg = StringField(label="Note message")
    submit = SubmitField(label = "Submit")




