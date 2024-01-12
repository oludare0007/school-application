import json, random, string, requests
from functools import wraps
import re
from flask import render_template,request,abort,redirect,flash,make_response,url_for,session,send_from_directory 
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import desc



#Local Imports
from main import app, csrf,mail,Message
from main.models import *
from main.forms import *

def generate_string(howmany): #call this function 
   x = random.sample(string.digits,howmany)
   return ''.join(x)

def login_required(f):
   @wraps(f) #This ensures that details(meta data) about the original function f, that is being decorated is still available
   def login_check(*args,**kwargs):
      if session.get("userloggedin") !=None:
         return f(*args,**kwargs)
      else:
         flash("Access Denied")
         return redirect('/login')
   return login_check






@app.route("/register/",methods=['GET','POST'])
def register():
    regform = RegForm()

    if request.method == "GET":
        return render_template("users/register.html", regform=regform)
    else:
        if regform.validate_on_submit():
            # Retrieve the form data
            fullname = request.form.get("fullname")
            email = request.form.get("email")
            pwd = request.form.get("pwd")

          
            existing_user = User.query.filter_by(user_email=email).first()
            if existing_user:
                flash("Email already exists. Please choose a different email.")
                return render_template("users/register.html", regform=regform)

            
            hashed_pwd = generate_password_hash(pwd)
            new_user = User(user_fullname=fullname, user_email=email, user_pwd=hashed_pwd)
            db.session.add(new_user)
            db.session.commit()
            flash("An account has been created for you. Please log in.")
            return redirect('/login')
        else:
            return render_template("users/register.html", regform=regform)

        


@app.route("/login/",methods=["POST","GET"])
def login():
    logform=LoginForm()
    if request.method=='GET':
        return render_template('users/login.html',logform=logform)
    
    else:
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        userdeets = db.session.query(User).filter(User.user_email==email).first()
        if userdeets != None:
            hashed_pwd = userdeets.user_pwd
            if check_password_hash(hashed_pwd, pwd) == True:
                session['userloggedin'] = userdeets.user_id
                return render_template("users/dashboard.html",logform=logform,userdeets=userdeets)
                
            else:
                flash("Invalid credentials, try again")
                return redirect("/login")
        else:

            flash("Invalid credentials, try again")
            return redirect("/login")
        

@app.route("/logout/")
def logout():
    if session.get('userloggedin') !=None:
        session.pop('userloggedin',None)
    return redirect("/login")



@app.route("/dashboard/")
@login_required
def dashboard():
    
        id = session.get('userloggedin')
        userdeets = User.query.get(id)
        return render_template("users/dashboard.html",userdeets=userdeets)



@app.route("/studentregform/",methods=['GET','POST'])
@login_required
def studentregform():
    studentregform = StudentForm()
    if request.method=="GET":
        return render_template("users/studentregform.html",studentregform=studentregform)
    else:
        if studentregform.validate_on_submit():
            #retrieve the form data and insert to user table
            id = session.get('userloggedin')
            firstname = request.values.get("firstname")  
            middlename = request.values.get("middlename") 
            lastname = request.values.get("lastname") 
            classname = request.values.get("classname") 
            dateofbirth = request.values.get('dateofbirth')   
            parentphoneno = request.values.get('parentphoneno') 
           
            users = Students(user_id=id,first_name=firstname,middle_name=middlename,last_name=lastname,date_of_birth=dateofbirth,parent_phone_no=parentphoneno,class_name=classname)
            
           
            
            db.session.add(users)
            db.session.commit()
            flash("Student records created successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("PLease Fill all Fields")
            return render_template("users/studentregform.html",studentregform=studentregform)





@app.route("/users/studentrecords/",methods=["POST","GET"])
@login_required
def studentrecords():
     id = session.get('userloggedin')
     students = db.session.query(Students).filter(Students.user_id == id ).all()

     return render_template('users/studentrecords.html',students=students)







@app.route("/edit/records/<int:id>", methods=["POST", "GET"])
@login_required
def edit_record(id):
    editform=EditForm()
    parent = session.get('userloggedin')
    student = db.session.query(Students).filter(Students.student_id == id).first_or_404()
    user = db.session.query(User).get(parent)
    
    if request.method == "GET":
        return render_template("users/editrecords.html", student=student,user=user,editform=editform)
    else:
        if editform.validate_on_submit():
            record_update = Students.query.get(id)
            record_update.first_name = request.form.get('firstname')
            record_update.middle_name = request.form.get('middlename')
            record_update.last_name = request.form.get('lastname')
            record_update.class_name = request.form.get('classname')
            record_update.date_of_birth= request.form.get('dateofbirth')   
            record_update.parent_phone_no= request.form.get('parentphoneno') 
            db.session.commit()
         
            flash("Student Records Updated")
            return redirect(url_for('studentrecords'))  
        else:
            flash("Student Records not updated")
            return render_template("/users/editrecords.html",editform=editform,user=user,student=student)

       
@app.route("/users/viewresults/<int:id>", methods=["POST", "GET"])
@login_required
def view_results(id):
    student = db.session.query(Students).filter(Students.student_id == id).first_or_404()
    parent = session.get('userloggedin')
    results = db.session.query(Result).filter(Result.student_id == id).all()
    user = db.session.query(User).get(parent)
    return render_template('users/viewresults.html',results=results,user=user,student=student)



@app.route('/download/<id>', methods=['GET'])
@login_required
def download_image(id):
    result = db.session.query(Result).filter(Result.result_id == id).first()
    # filename = result.result_image
    directory = '/static/resultsupload/'
    return send_from_directory(directory, result, as_attachment=True)




@app.route('/makepayments/<int:id>/',methods=["POST","GET"])
def makepayments(id):
    student = db.session.query(Students).filter(Students.student_id == id).first_or_404()
    if request.method=="GET":
        return render_template("users/payment.html",student=student)
    else:
        schoolfees = request.form.get('school')
        bookfees = request.form.get('book')
        uniformfees = request.form.get('uniform')
        aca_session = request.form.get('session')
        ref_no = generate_string(10)
        session['ref_no'] = ref_no
        userid = session.get('userloggedin')
        

        data = Payment(
            school_fees=schoolfees,
            books_fees=bookfees,
            uniform_fees=uniformfees,
            acc_session=aca_session,
            ref_no=ref_no,
            user_id = userid,
            student_id=student.student_id
        )

        db.session.add(data)
        db.session.commit()
        return redirect(url_for('confirm_payments'))
    
@app.route("/confirm_payments")
@login_required
def confirm_payments():
    if session.get('ref_no')==None: #when visited directly
        flash('please complete the form', category='error')
        return redirect(url_for('makepayments'))
    else:
        ref_no = session.get('ref_no', 'REF_NOT_FOUND')  # Replace 'REF_NOT_FOUND' with an appropriate fallback
        payment = db.session.query(Payment).filter(Payment.ref_no==ref_no).first_or_404()    
        return render_template('users/confirm_payments.html', ref_no=ref_no,payment=payment)



@app.route("/initialize/paystack/")
def initialize_paystack():  
    refno = session.get('ref_no')
    payment = db.session.query(Payment).filter(Payment.ref_no==refno).first_or_404()
    totalsum = payment.school_fees + payment.books_fees + payment.uniform_fees
    userid=session.get('userloggedin')
    userdeets = User.query.get(userid)   
     
    url="https://api.paystack.co/transaction/initialize"
    
    headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_9c1941ac96501014768857c7dfb26f7ac5e19bdd"}
    data={"email":userdeets.user_email, "amount":totalsum,"reference":refno}
    response = requests.post(url,headers=headers,data=json.dumps(data))   
    rspjson = response.json()    
    if rspjson['status'] == True:
        redirectURL = rspjson['data']['authorization_url']
        return redirect(redirectURL)
    
    else:
        flash("Please complete the form again")
        return redirect('/make_payment/')
    

@app.route("/landing")
def landing_page():
    refno = session.get('ref_no')
    payment = db.session.query(Payment).filter(Payment.ref_no==refno).first_or_404()
    totalsum = payment.school_fees + payment.books_fees + payment.uniform_fees
    userid=session.get('userloggedin')
    userdeets = User.query.get(userid)
    url="https://api.paystack.co/transaction/verify/"+refno
    headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_9c1941ac96501014768857c7dfb26f7ac5e19bdd"}
    response = requests.get(url,headers=headers)
    rspjson = json.loads(response.text)

    if rspjson['status'] == True:
        paystatus = rspjson['data']['gateway_response']
        ref_no = session.get('ref_no')

        # Update StudentFees status
        payment.payment_status = "Successful"
        db.session.commit()

        session.pop('ref_no',None)

        flash("Payment Successful", category="success")
        return redirect(url_for("studentrecords"))
    
    else:
        payment.payment_status = "Fail"
        db.session.commit()
       
        return redirect('confirm_payments')
    


@app.route("/users/viewdailyreport/<int:id>", methods=["GET"])
@login_required
def viewdailyreports(id):
    student_id = id
    daily_report = db.session.query(Dailyreport).filter_by(student_id=student_id) .order_by(desc(Dailyreport.sent_date)).first()
    all_reports = db.session.query(Dailyreport).filter_by(student_id=student_id).order_by(desc(Dailyreport.sent_date)).all()

    if daily_report:
        return render_template('users/viewdailyreport.html', report=daily_report,all_reports=all_reports)
    else:
        flash('Student has no daily report.')
        return render_template('users/viewdailyreport.html', report=None)
