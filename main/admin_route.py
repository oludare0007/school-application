

import random,os,string
import json
from functools import wraps
import re
from flask import render_template,request,abort,redirect,flash,make_response,url_for,session 
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import or_  



#Local Imports
from main import app, csrf,mail,Message
from main.models import *
from main.forms import *





def login_required(f):
    @wraps(f)#this ensures that details(meta data) about the original function f, that is being decorated is still available
    def login_check(*args,**kwargs):
        if session.get("adminuser") != None:
            return f(*args,**kwargs)
        else:
            flash("Access Denied")
            return redirect("/login")
    return login_check



@app.route("/admin/")
def admin_page():
   if session.get("adminuser") == None or session.get("role")  !='admin':
      return render_template("admin/adminlogin.html")
   else:
      return redirect(url_for('admin_dashboard'))




@app.route("/admin/adminlogin/",methods=["GET","POST"])
def admin_login():
   if request.method =='GET':
      return render_template('admin/adminlogin.html')
   else:
      #retrieve form data
      username = request.form.get("username")
      pwd = request.form.get("pwd")
      #check if it is in the database
      check = db.session.query(Admin).filter(Admin.admin_username==username,Admin.admin_pwd==pwd).first()
      
      #if it is in the db, save in session and redirect to dashboard
      if check: #It is indb, save session
         session['adminuser']=check.admin_id
         session['role']='admin'
         adminid = session.get('adminuser')
         admindeet = db.session.query(Admin).get_or_404(adminid)
         return render_template('admin/dashboard.html',check=check,admindeet=admindeet)
      else: #if not, save message in flash, redirect to login again
         flash('Invalid Login',category='error')
         return redirect(url_for('admin_login'))
      

@app.route("/admin/dashboard/")
@login_required
def admin_dashboard():
   admindeet = db.session.query(Admin).first()
   if session.get("adminuser") == None or session.get("role")  !='admin':
      return redirect(url_for("admin_login"))
   else:
      
      return render_template('admin/dashboard.html',admindeet=admindeet)
   


@app.route("/admin/logout")
def admin_logout():
   if session.get("adminuser") != None:
      session.pop("adminuser",None)
      session.pop("role",None)
      flash("You are logged out",category="info")
      return redirect(url_for("admin_login"))
   else:
      return redirect(url_for('admin_login'))
   


@app.route("/admin/allstudentrec/")
@login_required
def allstudentrec():
     students = db.session.query(Students).all()
     return render_template('admin/allstudentrec.html',students=students)




@app.route("/admin/editstudentrec/<int:id>", methods=["POST", "GET"])
@login_required
def editstudentrec(id):
   editform=EditForm()
   student = db.session.query(Students).filter(Students.student_id == id).first_or_404()
   if request.method == "GET":
        return render_template("admin/editstudentrec.html", student=student,editform=editform)
   else:
        if editform.validate_on_submit():
            record_update = Students.query.get(id)
            record_update.first_name = request.form.get('firstname')
            record_update.middle_name = request.form.get('middlename')
            record_update.last_name = request.form.get('lastname')
            record_update.date_of_birth= request.form.get('dateofbirth')   
            record_update.parent_phone_no= request.form.get('parentphoneno') 
            db.session.commit()
         
            flash("Student Records Updated")
            return redirect(url_for('allstudentrec'))  
        else:
            flash("Student Records not updated")
            return render_template("/admin/editstudentrec.html",editform=editform,student=student)
        
      



@app.route("/admin/delete/<int:id>")
@login_required
def studentrec_delete(id):
   student = db.session.query(Students).get_or_404(id)
   db.session.delete(student)
   db.session.commit()
   flash("Student record deleted")
   return redirect(url_for('allstudentrec'))







@app.route("/admin/search", methods=["GET", "POST"])
@login_required
def search_students():
    if request.method == "GET":
        search_query = request.args.get("searchname")
        
        results = Students.query.filter(
            or_(
                Students.first_name.ilike(f"%{search_query}%"),
                Students.last_name.ilike(f"%{search_query}%")
            )
        ).all()
        
        if results:
            flash("Record found")
        else:
            flash("Record not found")
        
        return render_template("/admin/search_results.html", results=results)
    else:
        flash("Record not found")
        return redirect(url_for('allstudentrec'))




    
@app.route("/admin/addresults/<int:id>", methods=["GET", "POST"])
@login_required
def addresults(id):
    if session.get("adminuser") is None or session.get("role") != "admin":
        return redirect(url_for("admin_login"))
    else:
        if request.method == "GET":
            results = db.session.query(Students).get_or_404(id)
            return render_template("admin/addresults.html", results=results)
        else:
            allowed = {"jpg", "png", "jpeg"}
            fileobj = request.files["result"]
            filename = fileobj.filename
            comments = request.form.get("txt")  # Get the comment from the form

            if filename == "":
                flash("Result was not uploaded")
                return redirect(url_for("addresults", id=id))
            else:
                pieces = filename.split(".")
                ext = pieces[-1].lower()

                if ext in allowed:
                    newname = str(int(random.random() * 1000000000)) + filename
                    fileobj.save("main/static/resultsupload/" + newname)

                    result = Result(
                        result_image=newname,
                        student_id=id,
                        result_comment=comments  # Add the comment to the Result model
                    )

                    db.session.add(result)
                    db.session.commit()

                    flash("Result and comment uploaded")
                    return redirect(url_for("allstudentrec"))
                else:
                    flash("File extension not allowed, file was not uploaded")
                    return redirect(url_for("allstudentrec"))
                

@app.route("/admin/dailycomments/<int:id>", methods=["GET", "POST"])
@login_required
def dailyreport(id):
     if session.get("adminuser") is None or session.get("role") != "admin":
        return redirect(url_for("admin_login"))
     else:
          if request.method == "GET":
            results = db.session.query(Students).get_or_404(id)
            return render_template("admin/dailycomments.html", results=results)
          else:
              comments = request.form.get("cmt")  # Get the comment from the form
              report = Dailyreport(
                        
                        student_id=id,
                        daily_report=comments  # Add the comment to the Result model
                    )

              db.session.add(report)
              db.session.commit()

              flash("Comment Sent")
              return redirect(url_for("allstudentrec"))
         

    




   

