# Flask Tools
from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from flask_login import login_required, current_user

# Database Models
from sqlalchemy.sql import func  # Import the 'func' module
from .models import User, Assignment, Code, User_Assignment, School, Notification, Note
from . import db

# Werkzeug tools
from werkzeug.utils import secure_filename

# Python Libraries
import json
import string
import os
import datetime as dt
import random
from datetime import datetime
import time

# My Libraries
from . import DateToolKit as ds
from . import TextRefinerMini as trm

# Get the current date
current_date = dt.date.today()
current_time = datetime.now().strftime("%H:%M")


# Format the date as "YYYY-MM-DD"
formatted_date = current_date.strftime("%Y-%m-%d")

date = formatted_date

time = current_time

views = Blueprint('views', __name__)

def abbreviatedName(name):
  return (trm.abbr(name=name, count=2)[0]).replace(" ", "")

def detectDeviceType(theRequest):
  user_agent = theRequest.user_agent.string.lower()

  if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
      device_type = 'Mobile'
  else:
      device_type = 'Desktop'

  return device_type

def retSS():
    Tschool = School.query.filter_by(id=current_user.SCI).first().id
    Tstudent = (User.query.filter_by(SJI=Tschool))
    Tstudents = len(list(Tstudent.all()))
    SA = User.query.filter_by(id=current_user.id).first().Slots
    TSR = SA - Tstudents

    TstudentModfied = User.query.filter_by(SJI=Tschool, who='Student')
    Tteachers = User.query.filter_by(SJI=Tschool, who='Teacher')

    NumberOfMembers = {
        'students': TstudentModfied.count(),
        'teachers': Tteachers.count()
    }

    assignments_basket = []

    for t in Tteachers.all():
        count = len(list(Assignment.query.filter_by(user_id=t.id).all()))
        assignments_basket.append(count)

    number_of_assignments = sum(assignments_basket)

    return [TSR, Tstudents, TstudentModfied.all(), NumberOfMembers, number_of_assignments, Tteachers.all()]

def detectGrade(grade):
  if grade in ["ss1", "sS1", "SS1", "Ss1", "ss2", "sS2", "SS2", "Ss2", "ss3", "sS3", "SS3", "Ss3"]:
    return 'senior'
  else:
    return 'junior'




@views.route('/')
def index():

  return render_template("base.html")


@views.route('/homeA')
@login_required
def homeA():
    notific = Notification.query.filter_by(adStatus="Handled").all()
    for nt in notific:
        db.session.delete(nt)
        db.session.commit()

    if current_user.who == "Teacher":
        flash("You Can't Access this page", category="Access Denied")

        return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, fAssignment="", uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

    elif current_user.who == "Student":
        flash("You Can't Access this page.", category="Access Denied")
        return render_template("ROAS2.html", pt=School.query.filter_by(id=current_user.SJI).first(), uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, grade=detectGrade(current_user.grade), fAssignment="")

    else:
        return render_template("AdminPage.html", number_of_assignments=retSS()[4], number_of_members=retSS()[3], current_user=current_user, current_app=current_app, current_date=ds.clean_date(formatted_date), current_time=current_time, radColor=random.choice(["#ff00009c", "#001dff9c", "#3dff009c", "#ffbe009c", "#9300ff9c", "#ffed009c", "#00ffe99c", "#89999db8"]), device=detectDeviceType(request), uanf=abbreviatedName, stus=retSS()[2], srm=retSS()[0], teachers=retSS()[5], stu=retSS()[1], ntf=Notification.query.filter_by(recipient_id=current_user.id).all(), sl=School.query.filter_by(user_id=current_user.id).first(), fAssignment="", uan=abbreviatedName(current_user.name), dateClean=ds)


@views.route('/set-account-type', methods=['GET', 'POST'])
def SAT():

    if request.method == "POST":
        accountType = request.form['accType']
        UID = request.form['stID']

        if accountType == "Student":
            User.query.filter_by(id=UID).first().who = "Student"

            db.session.commit()
            return redirect(url_for("students_actions.studentGate"))


        elif accountType == "Teacher":
            User.query.filter_by(id=UID).first().who = "Teacher"

            db.session.commit()
            return redirect(url_for("teachers_actions.gateT"))


        else:
            User.query.filter_by(id=UID).first().who = "Admin"
            User.query.filter_by(id=UID).first().PlanType = "Free"
            User.query.filter_by(id=UID).first().Slots = 5

            db.session.commit()
            
            return redirect(url_for("views.SlideForm"))

            # https://papershare.pythonanywhere.com/M8AZ8L7Y6
            # return render_template("AdminPage.html", number_of_members=retSS()[3], current_user=current_user, current_app=current_app, current_date=ds.clean_date(formatted_date), current_time=current_time)
        

    return render_template("signup-choose-type.html", current_user=current_user, current_app=current_app)


@views.route('/<tsl>')
@login_required
def serve_tsl(tsl):
    link = School.query.filter_by(link=f"https://papershare.pythonanywhere.com/{tsl}").first()

    if current_user.POAS == "Joined":
        return render_template("ROAS2.html", pt=School.query.filter_by(id=current_user.SJI).first(), uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, grade=detectGrade(current_user.grade), fAssignment="")
    elif current_user.POAS == None:
        if link:
            if current_user.who == "Student":
                user = User.query.filter_by(id=current_user.id).first()
                user.POAS = "Pending"
                db.session.commit()
                school_name = School.query.filter_by(link=f"https://papershare.pythonanywhere.com/{tsl}").first().name

                # Send Notification
                school_owner = School.query.filter_by(link=f"https://papershare.pythonanywhere.com/{tsl}").first().user
                if current_user.who == "Student":
                    notification_content = f"Student {current_user.name} has expressed interest in joining {school_name}. Please review the request and provide updates on the status."
                else:
                    notification_content = f"Teacher {current_user.name} has expressed interest in joining {school_name}. Please review the request and provide updates on the status."
                notification = Notification(sender=current_user, recipient=school_owner, content=notification_content, adStatus="Not Handled")
                db.session.add(notification)
                db.session.commit()

                # hereedew

                return render_template("gate.html", joinedStat="Pending", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)

            elif current_user.who == "Teacher":
                return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, fAssignment="", uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

            else:
                flash("No Account Yet! Created one today.", category="Error occurred")
                return render_template("login.html")

    else:
        return render_template("gate.html", joinedStat="No Application Sent Yet", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)


    flash("Link not found.", category="Error occurred")
    return render_template("login.html")

@views.route('/ad-applicant/<aID>', methods=['GET', 'POST'])
@login_required
def candidateFate(aID):
    notific = Notification.query.filter_by(sender_id=aID).all()
    for nt in notific:
        nt.adStatus = "Handled"
    db.session.commit()

    if request.method == "POST":
        cause = request.form['action']


        if cause == "Accept":
            if retSS()[0] == 0:
                flash("Sorry, but you've reached the maximum number of students you can accommodate for this your current plan.", category="Slot Full")
                userToDec = User.query.filter_by(id=aID).first()
                userToDec.POAS = "Declined"
                db.session.commit()

                # flash(f"Successfully declined the request from {userToDec.name}.", category="Success")

            elif retSS()[0] > 5:
                userToAcc = User.query.filter_by(id=aID).first()
                userToAcc.POAS = "Joined"
                userToAcc.SJI = User.query.filter_by(id=current_user.id).first().SCI
                db.session.commit()

                flash(f"Slots remaining is less than 5. Successfully accepted the request from {userToAcc.name}.", category="Important")
            else:
                userToAcc = User.query.filter_by(id=aID).first()
                userToAcc.POAS = "Joined"
                userToAcc.SJI = User.query.filter_by(id=current_user.id).first().SCI
                db.session.commit()

                flash(f"Successfully accepted the request from {userToAcc.name}.", category="Success")
        else:
            userToDec = User.query.filter_by(id=aID).first()
            userToDec.POAS = "Declined"
            db.session.commit()

            flash(f"Successfully declined the request from {userToDec.name}.", category="Success")



        return redirect(url_for("views.homeA"))


    return redirect(url_for("views.homeA"))



@views.route('/tosa', methods=['GET', 'POST'])
@login_required
def adminAction():
    if request.method == "POST":
        studentID = request.form['sID']
        Student = User.query.filter_by(id=studentID).first()
        atac = Assignment.query.filter_by(user_id=current_user.id).all()
        atacc = {}
        sas = []
        for a in atac:
            atacc[f'{a.name}'] = (a.code)

        uaq = User_Assignment.query.filter_by(user_id=studentID).all()
        sas = len(list(uaq))

        imsa = True

        return render_template("studentDetail.html", wtr=[atacc, sas, imsa], current_user=current_user, current_app=current_app, Student=Student, an=abbreviatedName, radColor=random.choice(["#ff00009c", "#001dff9c", "#3dff009c", "#ffbe009c", "#9300ff9c", "#ffed009c", "#00ffe99c", "#89999db8"]))

    try:
        return redirect(url_for("views.homeA"))
    except:
        return render_template("AdminPage.html", number_of_assignments=retSS()[4], number_of_members=retSS()[3], current_user=current_user, current_app=current_app, current_date=ds.clean_date(formatted_date), current_time=current_time, radColor=random.choice(["#ff00009c", "#001dff9c", "#3dff009c", "#ffbe009c", "#9300ff9c", "#ffed009c", "#00ffe99c", "#89999db8"]), device=detectDeviceType(request), uanf=abbreviatedName, stus=retSS()[2], srm=retSS()[0], teachers=retSS()[5], stu=retSS()[1], ntf=Notification.query.filter_by(recipient_id=current_user.id).all(), sl=School.query.filter_by(user_id=current_user.id).first(), fAssignment="", uan=abbreviatedName(current_user.name), dateClean=ds)

@views.route('/remove-student/<int:studentId>')
@login_required
def removeStudent(studentId):
    Student = User.query.filter_by(id=studentId).first()
    Student.SJI = None
    Student.POAS = "Declined"
    db.session.commit()

    flash(f"Successfully removed {Student.name}.", category="Removed Student")

    
    try:
        return redirect(url_for("views.homeA"))
    except:
        return render_template("AdminPage.html", number_of_assignments=retSS()[4], number_of_members=retSS()[3], current_user=current_user, current_app=current_app, current_date=ds.clean_date(formatted_date), current_time=current_time, radColor=random.choice(["#ff00009c", "#001dff9c", "#3dff009c", "#ffbe009c", "#9300ff9c", "#ffed009c", "#00ffe99c", "#89999db8"]), device=detectDeviceType(request), uanf=abbreviatedName, stus=retSS()[2], srm=retSS()[0], teachers=retSS()[5], stu=retSS()[1], ntf=Notification.query.filter_by(recipient_id=current_user.id).all(), sl=School.query.filter_by(user_id=current_user.id).first(), fAssignment="", uan=abbreviatedName(current_user.name), dateClean=ds)

@views.route('/create-school', methods=['GET', 'POST'])
@login_required
def createSchool():

  # tcontent = request.form['content']
  schoolName = request.form['name']
  schoolEmail = request.form['email']
  schoolDescription = request.form['description']
  schoolLink = request.form['link']

  try:
    newSchool = School(name=schoolName, email=schoolEmail, description=schoolDescription, link=schoolLink, user_id=current_user.id)
    db.session.add(newSchool)
    User.query.filter_by(id=current_user.id).first().SCI = School.query.filter_by(email=schoolEmail).first().id
    db.session.commit()

    

    flash(f"{schoolName} School Created Successfully", category="Success")


    return render_template("Plans-page.html", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)
  except:

    flash(f"Something went wrong while creating {schoolName}!", category="Error occurred")


    return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, fAssignment="", uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

@views.route('/SlideForm-cs')
@login_required
def SlideForm():

  letters = list(string.ascii_uppercase)
  numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
  AlphaNum = f"{random.choice(letters)}{random.choice(numbers)}{random.choice(letters)}{random.choice(letters)}{random.choice(numbers)}{random.choice(letters)}{random.choice(numbers)}{random.choice(letters)}{random.choice(numbers)}"

  schoolLink = f"https://papershare.pythonanywhere.com/{AlphaNum}"

  return render_template("SlideForm.html", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time, device=detectDeviceType(request), sl=schoolLink)

# Add a route to serve uploaded images
@views.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
  return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@views.route('/plan-choose')
@login_required
def redirectToChoosePlanForm():

  # flash("Which Country?", category='Country?')

  return render_template("Plans-page.html", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time, device=detectDeviceType(request))

  # valid_verifications_number = [
  #           "200354EDRD32",
  #           "526378YTERS32",
  #           "781123HGAS91",
  #           "124453OPQW91",
  #           "987654XYZA21",
  #           "345678JKLP87",
  #           "654321MNOB54",
  #           "890123QRST65",
  #           "234567UVWI43"
  #       ]








@views.route('/blog')
def showBlogPage():
    
    flash("Blogs coming soon", category="Blogs")

    return render_template("blogPage.html")