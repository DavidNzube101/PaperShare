# Flask Modules
from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

# Database Models
from .models import User, Assignment, Code, User_Assignment, School, Notification, Note
from . import db

# Flask Modules
from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

# Database Models
from .models import User, Assignment, Code, User_Assignment, School, Notification, Note
from . import db

# Python Modules
import random

import json
import string
import os
import datetime as dt
from datetime import datetime
import time

# My Modules
from . import DateToolKit as ds
from . import TextRefinerMini as trm


# Getting Date-Time Info
current_date = dt.date.today()
current_time = datetime.now().strftime("%H:%M")

# Date Format: "YYYY-MM-DD"
formatted_date = current_date.strftime("%Y-%m-%d")
date = formatted_date
time = current_time

students_actions = Blueprint('students_actions', __name__)


# Functions to perform basic tasks
def abbreviatedName(name):
  return trm.abbr(name=name, count=2)[0]

def detectGrade(grade):
  if grade in ["ss1", "sS1", "SS1", "Ss1", "ss2", "sS2", "SS2", "Ss2", "ss3", "sS3", "SS3", "Ss3"]:
    return 'senior'
  else:
    return 'junior'

def validateDate(dos_date, dos_time, deadline_date, deadline_time):
    dos = datetime.strptime(f"{dos_date} {dos_time}", "%Y-%m-%d %H:%M")
    deadline = datetime.strptime(f"{deadline_date} {deadline_time}", "%Y-%m-%d %H:%M")
    return dos <= deadline


@students_actions.route('/home')
@login_required
def home():
    if current_user.who == "Teacher":
        flash("You Can't Access this page", category="Access Denied")

        return redirect(url_for("teachers_actions.homeT"))

    elif current_user.who == "Admin":
        return redirect(url_for("views.homeA"))

    else:
        if current_user.POAS == "Joined":

            return render_template("ROAS2.html", pt=School.query.filter_by(id=current_user.SJI).first(), uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, grade=detectGrade(current_user.grade), fAssignment="")

        else:
            # flash("You haven't joined a school yet.", category="Important")
            if current_user.POAS is None:
                cup = "No Requests Yet"
            else:
                cup = current_user.POAS
            return render_template("gate.html", joinedStat=cup, current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)



@students_actions.route('/gate', methods=['GET', 'POST'])
@login_required
def studentGate():
    if ((current_user.POAS == "Pending")):
        if request.method == "POST":

            links = [link[0] for link in School.query.with_entities(School.link).all()]  # Extracting links from tuples
            link = request.form['code']

            if link in links:
                user = User.query.filter_by(id=current_user.id).first()
                user.POAS = "Pending"
                db.session.commit()
                school_name = School.query.filter_by(link=link).first().name

                # Send Notification
                school_owner = School.query.filter_by(link=link).first().user
                if current_user.who == "Student":
                    notification_content = f"Student {current_user.name} has expressed interest in joining {school_name}. Please review the request and provide updates on the status."
                else:
                    notification_content = f"Teacher {current_user.name} has expressed interest in joining {school_name}. Please review the request and provide updates on the status."
                notification = Notification(sender=current_user, recipient=school_owner, content=notification_content, adStatus="Not Handled")
                db.session.add(notification)
                db.session.commit()

                flash(f"You have successfully sent a request to join {school_name}. Please check back soon and Refresh Status to update the status of your application.", category="Success")

                return render_template("gate.html", joinedStat="Pending", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)
            else:
                flash("We're sorry, but you can't join the school associated with that link. Possible reasons include an invalid link, a full quota of participants, or access denial by your teacher.", category="Error occurred")
                return render_template("gate.html", joinedStat="Declined", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)

        else:
            flash("Please wait for a response from your School. Your application is pending.", category="Application Pending")

            return render_template("gate.html", joinedStat="Pending", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)

    if (current_user.POAS == None):

        if request.method == "POST":

            links = [link[0] for link in School.query.with_entities(School.link).all()]  # Extracting links from tuples
            link = request.form['code']

            if link in links:
                user = User.query.filter_by(id=current_user.id).first()
                user.POAS = "Pending"
                db.session.commit()
                school_name = School.query.filter_by(link=link).first().name

                # Send Notification
                school_owner = School.query.filter_by(link=link).first().user
                if current_user.who == "Student":
                    notification_content = f"Student {current_user.name} has expressed interest in joining {school_name}. Please review the request and provide updates on the status."
                else:
                    notification_content = f"Teacher {current_user.name} has expressed interest in joining {school_name}. Please review the request and provide updates on the status."
                notification = Notification(sender=current_user, recipient=school_owner, content=notification_content, adStatus="Not Handled")
                db.session.add(notification)
                db.session.commit()

                flash(f"You have successfully sent a request to join {school_name}. Please check back soon and Refresh Status to update the status of your application.", category="Success")

                return render_template("gate.html", joinedStat="Pending", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)
            else:
                flash("Sorry, but you can't join the school associated with that link. Possible reasons include an invalid link, a full quota of participants, or access denial by your teacher.", category="Error occurred")
                return render_template("gate.html", joinedStat="Denied", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)

        return render_template("gate.html", joinedStat="No Application Sent Yet", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)

    elif current_user.POAS == "Joined":

        return render_template("gate.html", joinedStat="Joined", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)

    elif current_user.POAS == "Declined":

        if request.method == "POST":

            links = [link[0] for link in School.query.with_entities(School.link).all()]  # Extracting links from tuples
            link = request.form['code']

            if link in links:
                user = User.query.filter_by(id=current_user.id).first()
                user.POAS = "Pending"
                db.session.commit()
                school_name = School.query.filter_by(link=link).first().name

                # Send Notification
                school_owner = School.query.filter_by(link=link).first().user
                if current_user.who == "Student":
                    notification_content = f"Student {current_user.name} has expressed interest in joining {school_name}. Please review the request and provide updates on the status."
                else:
                    notification_content = f"Teacher {current_user.name} has expressed interest in joining {school_name}. Please review the request and provide updates on the status."
                notification = Notification(sender=current_user, recipient=school_owner, content=notification_content, adStatus="Not Handled")
                db.session.add(notification)
                db.session.commit()

                flash(f"You have successfully sent a request to join {school_name}. Please check back soon and Refresh Status to update the status of your application.", category="Success")

                return render_template("gate.html", joinedStat="Pending", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)
            else:
                flash("Sorry, but you can't join the school associated with that link. Possible reasons include an invalid link, a full quota of participants, or access denial by your teacher.", category="Error occurred")
                return render_template("gate.html", joinedStat="Denied", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)


        else:
            flash("Sorry, your previous application was declined by your school.", category="Application Declined")

            User.query.filter_by(id=current_user.id).first().POAS = "Declined"

            return render_template("gate.html", joinedStat="Declined", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)


    else:

        if current_user.POAS is None:
            cup = "No Requests Yet"
        else:
            cup = current_user.POAS
        return render_template("gate.html", joinedStat=cup, current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)



@students_actions.route('/fetch-assignment', methods=['GET', 'POST'])
@login_required
def fetch():
  code = ""
  if request.method == 'POST':
    code = request.form['assCode']


    try:
      try:
        validateCode = Code.query.filter_by(codeNumber=int(code)).first()
        theAssignment = Assignment.query.filter_by(id=validateCode.assID).first()
      except ValueError:
        theAssignment = "empty"

    except AttributeError:
      theAssignment = "ocde"

    return render_template("ROAS2.html", pt=School.query.filter_by(id=current_user.SJI).first(), uan=abbreviatedName(current_user.name), current_code=code, current_time=time, current_date=date, current_user=current_user, grade=detectGrade(current_user.grade), fAssignment=theAssignment)

  return render_template("ROAS2.html", pt=School.query.filter_by(id=current_user.SJI).first(), uan=abbreviatedName(current_user.name), current_code=code, current_time=time, current_date=date, current_user=current_user, grade=detectGrade(current_user.grade), fAssignment="")


@students_actions.route('/submit-assignment', methods=['POST'])
@login_required
def submit():
    if request.method == 'POST':
        try:
            Name = request.form['user_name']
            Email = request.form['email']
            Date = request.form['date']
            Time = request.form['time']
            Ccode = request.form['numCode']
            Content = request.form['content']
            Image = request.files['inpFile']

            if Image and allowed_files(Image.filename):
                filename = secure_filename(Image.filename)
                Image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                filename_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')

                tCode = Code.query.filter_by(codeNumber=int(Ccode)).first()
                assLiToC = Assignment.query.filter_by(code=int(Ccode)).first()

                assDD = assLiToC.deadlineDate
                assDT = assLiToC.deadlineTime

                try:
                    if validateDate(dos_date=Date, dos_time=Time, deadline_date=assDD, deadline_time=assDT):
                        new_project = User_Assignment(user_id=current_user.id, linkCode=tCode.id, name=Name, email=Email, code=int(Ccode),  date=Date, time=Time, data=Content, image=filename, image_path=filename_path)
                        db.session.add(new_project)
                        db.session.commit()

                        whichAss = Assignment.query.filter_by(code=int(Ccode)).first()
                        whichUA = User_Assignment.query.filter_by(email=Email).first()

                        aeCode = Code.query.filter_by(codeNumber=int(Ccode)).first()
                        aeCode.submittedAssID = whichUA.id
                        db.session.commit()
                        flash("Submitted Successfully", category="Success")

                    else:
                        flash("Assignment not submitted!", category="Deadline reached")
                except:
                    new_project = User_Assignment(user_id=current_user.id, linkCode=tCode.id, name=Name, email=Email, code=int(Ccode),  date=Date, time=Time, data=Content, image=filename, image_path=filename_path)
                    db.session.add(new_project)
                    db.session.commit()

                    whichAss = Assignment.query.filter_by(code=int(Ccode)).first()
                    whichUA = User_Assignment.query.filter_by(email=Email).first()

                    aeCode = Code.query.filter_by(codeNumber=int(Ccode)).first()
                    aeCode.submittedAssID = whichUA.id
                    db.session.commit()
                    flash("Submitted Successfully", category="Success")

            else:
                filename = ""
                filename_path = ""
                tCode = Code.query.filter_by(codeNumber=int(Ccode)).first()

                assLiToC = Assignment.query.filter_by(code=int(Ccode)).first()

                assDD = assLiToC.deadlineDate
                assDT = assLiToC.deadlineTime

                try:
                    if validateDate(dos_date=Date, dos_time=Time, deadline_date=assDD, deadline_time=assDT):
                        new_project = User_Assignment(user_id=current_user.id, linkCode=tCode.id, name=Name, email=Email, code=int(Ccode),  date=Date, time=Time, data=Content, image=filename, image_path=filename_path)
                        db.session.add(new_project)
                        db.session.commit()

                        whichAss = Assignment.query.filter_by(code=int(Ccode)).first()
                        whichUA = User_Assignment.query.filter_by(email=Email).first()

                        aeCode = Code.query.filter_by(codeNumber=int(Ccode)).first()
                        aeCode.submittedAssID = whichUA.id
                        db.session.commit()
                        flash("Submitted Successfully", category="Success")

                    else:
                        flash("Assignment not submitted!", category="Deadline reached")
                except:
                    new_project = User_Assignment(user_id=current_user.id, linkCode=tCode.id, name=Name, email=Email, code=int(Ccode),  date=Date, time=Time, data=Content, image=filename, image_path=filename_path)
                    db.session.add(new_project)
                    db.session.commit()

                    whichAss = Assignment.query.filter_by(code=int(Ccode)).first()
                    whichUA = User_Assignment.query.filter_by(email=Email).first()

                    aeCode = Code.query.filter_by(codeNumber=int(Ccode)).first()
                    aeCode.submittedAssID = whichUA.id
                    db.session.commit()
                    flash("Submitted Successfully", category="Success")

        except Exception as e:
            flash(f'Error: {str(e)}', category="Error occurred")

    else:
        flash("Error Occurred. Try Again", category="Error occurred")

    return render_template("ROAS2.html", pt=School.query.filter_by(id=current_user.SJI).first(), uan=abbreviatedName(current_user.name), current_code=000000, current_time=time, current_date=date, current_user=current_user, grade=detectGrade(current_user.grade), fAssignment="")

def allowed_files(filename):
  return True



@students_actions.route('/updateInfoS', methods=['GET', 'POST'])
@login_required
def updateInfoS():
  if request.method == 'POST':
    user_name = request.form['name']
    email = request.form['email']
    userType = request.form['userType']

    theuser = User.query.filter_by(id=current_user.id).first()

    theuser.name=user_name
    theuser.email=email
    theuser.who=userType
    db.session.commit()

    flash("Updated Info", category="Success")

    try:
        return redirect(url_for("students_actions.home"))
    except:
        return render_template("ROAS2.html", pt=School.query.filter_by(id=current_user.SJI).first(), uan=abbreviatedName(current_user.name), current_code=000000, current_time=current_time, current_date=formatted_date, current_user=current_user, grade=detectGrade(current_user.grade), fAssignment="")

  return render_template("ROAS2.html", pt=School.query.filter_by(id=current_user.SJI).first(), uan=abbreviatedName(current_user.name), current_code=000000, current_time=current_time, current_date=formatted_date, current_user=current_user, grade=detectGrade(current_user.grade), fAssignment="")




