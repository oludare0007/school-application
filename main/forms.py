from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, PasswordField,DateField,IntegerField, SelectField
from wtforms.validators import Email, DataRequired, EqualTo, Length


class RegForm(FlaskForm):
   fullname = StringField("Fullname",validators=[DataRequired(message="The firstname is a must")])   
   email = StringField("Email",validators=[Email(message="Invalid Email Format"),DataRequired(message="Email must be supplied")])
   pwd = PasswordField("Enter Password",validators=[DataRequired()])
   confirmpwd = PasswordField("Confirm Password",validators=[EqualTo('pwd',message="Let the two password match")])  
   btnsubmit = SubmitField("Register!")


class LoginForm(FlaskForm):
    email = StringField("Email",validators=[Email(message="Invalid Email Format"),DataRequired(message="Email must be supplied")])
    pwd = PasswordField("Enter Password",validators=[DataRequired()])
    btnsubmit = SubmitField("Login")


class StudentForm(FlaskForm):
    firstname = StringField("Firstname",validators=[DataRequired(message="The firstname is a must")])
    middlename = StringField("Middlename",validators=[DataRequired(message="The middlename is a must")])
    lastname = StringField("Lastname",validators=[DataRequired(message="The lastname is a must")])
    classname = StringField("Classname",validators=[DataRequired(message="Input class name")])
    dateofbirth = DateField("Date of Birth", format="%Y-%m-%d", validators=[DataRequired(message="The date of birth is required")])
    classname = StringField("Classname",validators=[DataRequired(message="The Classname is a must")])
    parentphoneno = IntegerField("Parent's Phone Number", validators=[DataRequired(message="The parent's phone number is required")])
    btnsubmit = SubmitField("Submit")


class EditForm(FlaskForm):
    firstname = StringField("Firstname",validators=[DataRequired(message="The firstname is a must")])
    middlename = StringField("Middlename",validators=[DataRequired(message="The middlename is a must")])
    lastname = StringField("Lastname",validators=[DataRequired(message="The lastname is a must")])
    classname = StringField("Classname",validators=[DataRequired(message="Input class name")])
    dateofbirth = DateField("Date of Birth", format="%Y-%m-%d", validators=[DataRequired(message="The date of birth is required")])
    classname = StringField("Classname",validators=[DataRequired(message="The Classname is a must")])
    parentphoneno = IntegerField("Parent's Phone Number", validators=[DataRequired(message="The parent's phone number is required")])
    btnsubmit = SubmitField("Submit")




class Loginform(FlaskForm):
    classname = StringField("Classname",validators=[DataRequired(message="Input class name")])
    
   