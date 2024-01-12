from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()




class User(db.Model):  
    user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_fullname = db.Column(db.String(100),nullable=False)
    user_email = db.Column(db.String(120)) 
    user_pwd=db.Column(db.String(120),nullable=True)
    user_datereg=db.Column(db.DateTime(), default=datetime.utcnow)
    users_students = db.relationship("Students", back_populates='students_users')
    


class Students(db.Model):
    student_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    first_name = db.Column(db.String(100),nullable=False)
    middle_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    class_name = db.Column(db.String(100),nullable=False)
    date_of_birth = db.Column(db.Date(),nullable=False)
    parent_phone_no = db.Column(db.String(30),nullable=False)
    date_of_reg = db.Column(db.DateTime(),default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)  
    students_users = db.relationship("User", back_populates='users_students')
  
   

class Class(db.Model):

    class_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    class_name = db.Column(db.String(100),nullable=False)

class Payment(db.Model):
    payment_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    acc_session = db.Column(db.String(100),nullable=False)
    school_fees = db.Column(db.Float,nullable=False)
    books_fees =  db.Column(db.Float,nullable=False)
    uniform_fees =  db.Column(db.Float,nullable=False)
    payment_status = db.Column(db.Enum('Successful','Fail','Pending'), default='Pending')
    ref_no = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False) 
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'),nullable=False) 


class Admin(db.Model):
    admin_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_username=db.Column(db.String(20),nullable=True)
    admin_pwd=db.Column(db.String(200),nullable=True)


class Result(db.Model):
     result_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
     result_image = db.Column(db.String(100))
     result_comment = db.Column(db.String(200),nullable=False)
     student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'),nullable=False)
     sent_date=db.Column(db.DateTime(), default=datetime.utcnow)


class Dailyreport(db.Model):
     daily_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
     daily_report = db.Column(db.String(200),nullable=False)
     student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'),nullable=False)
     sent_date=db.Column(db.DateTime(), default=datetime.utcnow)

    
    


