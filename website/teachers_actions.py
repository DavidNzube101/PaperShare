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


# Initializing Blueprint
teachers_actions = Blueprint('teachers_actions', __name__)

# Functions to perform basic tasks and return valuable information
def abbreviatedName(name):
  return trm.abbr(name=name, count=2)[0]

def retNotes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    # nosa = len(list(User_Assignment))

    return [notes]

def generateCode():
  code = ""
  for i in range(6):
    code += str(random.randint(0, 9))

  loc = Code.query.filter_by(codeNumber=int(code))

  if int(code) in list(loc):
    code = ""
    for i in range(6):
      code += str(random.randint(0, 9))

    return code

  else:
    return code


@teachers_actions.route('/homeT')
@login_required
def homeT():

    if current_user.who == "Student":
        flash("You Can't Access this page.", category="Access Denied")
        return redirect(url_for("students_actions.home"))

    elif current_user.who == "Admin":
        return redirect(url_for("views.homeA"))

    else:
        if current_user.POAS == "Joined":

            return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, fAssignment="", uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

        else:
            # flash("You haven't joined a school yet.", category="Important")
            if current_user.POAS is None:
                cup = "No Requests Yet"
            else:
                cup = current_user.POAS
            return render_template("gateT.html", joinedStat=cup, current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)


@teachers_actions.route('/gateT', methods=['GET', 'POST'])
@login_required
def gateT():


    
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

                return render_template("gateT.html", joinedStat="Pending", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)
            else:
                flash("Sorry, but you can't join the school associated with that link. Possible reasons include an invalid link, a full quota of participants, or access denial by your teacher.", category="Error occurred")
                return render_template("gate.html", joinedStat="Denied", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)

        return render_template("gateT.html", joinedStat="No Application Sent Yet", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)

    elif current_user.POAS == "Joined":

        return render_template("gateT.html", joinedStat="Joined", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)

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

                return render_template("gateT.html", joinedStat="Pending", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)
            else:
                flash("Sorry, but you can't join the school associated with that link. Possible reasons include an invalid link, a full quota of participants, or access denial by your teacher.", category="Error occurred")
                return render_template("gate.html", joinedStat="Denied", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)


        else:
            flash("Sorry, your previous application was declined by your school.", category="Application Declined")

            User.query.filter_by(id=current_user.id).first().POAS = "Declined"

            return render_template("gateT.html", joinedStat="Declined", current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)


    if current_user.POAS is None:
        cup = "No Requests Yet"
    else:
        cup = current_user.POAS
    return render_template("gateT.html", joinedStat=cup, current_user=current_user, current_app=current_app, current_date=ds.clean_date(date), current_time=current_time)



@teachers_actions.route('/create-note', methods=['GET', 'POST'])
@login_required
def createNote():
    
    if request.method == "POST":
        newNote = Note(name="Note 1", content="Note Content Goes here", user_id=current_user.id)

        db.session.add(newNote)
        db.session.commit()

        flash("New Note Created.", category="Created Note")

    try:
        return redirect(url_for('teachers_actions.homeT'))
    except:
        return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)


@teachers_actions.route('/remove-note/<int:noteId>', methods=['GET', 'POST'])
@login_required
def removeNote(noteId):
    
    thwNote = Note.query.filter_by(id=noteId).first()

    db.session.delete(thwNote)
    db.session.commit()

    flash("Deleted Note.", category="Deleted Note")

    try:
        return redirect(url_for('teachers_actions.homeT'))
    except:
        return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)


@teachers_actions.route('/create-assignment', methods=['GET', 'POST'])
@login_required
def create():
  if request.method == 'POST':
    userPlan = User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first().PlanType
    if userPlan == "Free":

        if len(list(Assignment.query.filter_by(user_id=current_user.id).all())) <= 2:
            code = request.form['assCode']
            subject = request.form['subject']
            content = request.form['content']
            image = request.files['inpFile']
            ddD = request.form['deadlineDate']
            ddT = request.form['deadlineTime']

            loc = Code.query.filter_by(codeNumber=int(code))

            if int(code) in list(loc):
              code = generateCode()

            else:
              pass


            if image and allowed_file(image.filename):
              filename = secure_filename(image.filename)
              image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
              filename_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')

              new_assignment = Assignment(user_id=current_user.id, name=(subject.capitalize()), data=content, image=filename, image_path=filename_path, code=int(code), deadlineDate=ddD, deadlineTime=ddT)
              db.session.add(new_assignment)

              db.session.commit()

              whichAss = Assignment.query.filter_by(code=int(code)).first()

              assign_code = Code(codeNumber=int(code), assID=whichAss.id)
              db.session.add(assign_code)

              db.session.commit()

            else:
              filename = ""
              filename_path = ""

              new_project = Assignment(user_id=current_user.id, name=(subject.capitalize()), data=content, image=filename, image_path=filename_path, code=int(code), deadlineDate=ddD, deadlineTime=ddT)
              db.session.add(new_project)
              db.session.commit()

              whichAss = Assignment.query.filter_by(code=int(code)).first()

              assign_code = Code(codeNumber=int(code), assID=whichAss.id)
              db.session.add(assign_code)

              db.session.commit()


            flash(f"Created `{subject.capitalize()}` Assignment!", category="Success")

        elif len(list(Assignment.query.filter_by(user_id=current_user.id).all())) > 2:
            flash(f"Sorry {current_user.name}, assignment not created. Your School is on a free plan and you've created the maximum number of assignments for your School's plan type.", category="Package Restriction")

        else:
            if User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first().activationStatus == "Verified":
              code = request.form['assCode']
              subject = request.form['subject']
              content = request.form['content']
              image = request.files['inpFile']
              ddD = request.form['deadlineDate']
              ddT = request.form['deadlineTime']

              loc = Code.query.filter_by(codeNumber=int(code))

              if int(code) in list(loc):
                code = generateCode()

              else:
                pass


              if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                filename_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')

                new_assignment = Assignment(user_id=current_user.id, name=(subject.capitalize()), data=content, image=filename, image_path=filename_path, code=int(code), deadlineDate=ddD, deadlineTime=ddT)
                db.session.add(new_assignment)

                db.session.commit()

                whichAss = Assignment.query.filter_by(code=int(code)).first()

                assign_code = Code(codeNumber=int(code), assID=whichAss.id)
                db.session.add(assign_code)

                db.session.commit()

              else:
                filename = ""
                filename_path = ""

                new_project = Assignment(user_id=current_user.id, name=(subject.capitalize()), data=content, image=filename, image_path=filename_path, code=int(code), deadlineDate=ddD, deadlineTime=ddT)
                db.session.add(new_project)
                db.session.commit()

                whichAss = Assignment.query.filter_by(code=int(code)).first()

                assign_code = Code(codeNumber=int(code), assID=whichAss.id)
                db.session.add(assign_code)

                db.session.commit()


              flash(f"Created `{subject.capitalize()}` Assignment!, {len(list(User_Assignment.query.filter_by(user_id=current_user.id).all()))}", category="Success")

            else:
              flash("Assignment not created. School's account not verified to start creating assignments.", category="Unverified Account")


    elif User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first().PlanType in ["Mini", "Large", "Premium"]:
        code = request.form['assCode']
        subject = request.form['subject']
        content = request.form['content']
        image = request.files['inpFile']
        ddD = request.form['deadlineDate']
        ddT = request.form['deadlineTime']

        loc = Code.query.filter_by(codeNumber=int(code))

        if int(code) in list(loc):
          code = generateCode()

        else:
          pass


        if image and allowed_file(image.filename):
          filename = secure_filename(image.filename)
          image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
          filename_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')

          new_assignment = Assignment(user_id=current_user.id, name=(subject.capitalize()), data=content, image=filename, image_path=filename_path, code=int(code), deadlineDate=ddD, deadlineTime=ddT)
          db.session.add(new_assignment)

          db.session.commit()

          whichAss = Assignment.query.filter_by(code=int(code)).first()

          assign_code = Code(codeNumber=int(code), assID=whichAss.id)
          db.session.add(assign_code)

          db.session.commit()

        else:
          filename = ""
          filename_path = ""

          new_project = Assignment(user_id=current_user.id, name=(subject.capitalize()), data=content, image=filename, image_path=filename_path, code=int(code), deadlineDate=ddD, deadlineTime=ddT)
          db.session.add(new_project)
          db.session.commit()

          whichAss = Assignment.query.filter_by(code=int(code)).first()

          assign_code = Code(codeNumber=int(code), assID=whichAss.id)
          db.session.add(assign_code)

          db.session.commit()


        flash(f"Created `{subject.capitalize()}` Assignment!", category="Success")
    


  else:
    flash("Error Occurred. Try Again", category="Error occurred")

    try:
      return redirect(url_for('teachers_actions.homeT'))
    except:
      return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)


  try:
    return redirect(url_for('teachers_actions.homeT'))
  except:
    return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

def allowed_file(filename):
    return True

@teachers_actions.route('/thread/<int:thecode>')
@login_required
def showAssignmentThread(thecode):
  theCode = Code.query.filter_by(codeNumber=thecode).first()
  submittedAssignments = User_Assignment.query.filter_by(code=thecode)


  return render_template('thread_page.html', sas=submittedAssignments, tc=theCode, current_time=time, current_date=date, current_user=current_user, nos=len(list(submittedAssignments)), bullet=trm)



@teachers_actions.route('/update/<int:assID>', methods=['GET', 'POST'])
@login_required
def update(assID):
  if request.method == 'POST':

    newName = request.form['name']
    newContent = request.form['description']
    newDD = request.form['deadlineDate']
    newDT = request.form['deadlineTime']

    theAssignment = Assignment.query.filter_by(id=(assID)).first()

    try:
      theAssignment.name=newName
      theAssignment.data=newContent
      theAssignment.deadlineDate=newDD
      theAssignment.deadlineTime=newDT
      db.session.commit()
      flash("Updated Assignment", category="Success")
    except:
      flash("Assignment Not Updated", category="Error occurred")

    return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

  try:
      return redirect(url_for('teachers_actions.homeT'))
  except:
    return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)


@teachers_actions.route('/updateInfo', methods=['GET', 'POST'])
@login_required
def updateInfo():
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
        return redirect(url_for("teachers_actions.homeT"))
    except:
        return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

  return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)




@teachers_actions.route('/delete-created-assignment', methods=['GET', 'POST'])
@login_required
def delAss():

    if len(list(Assignment.query.filter_by(user_id=current_user.id).all())) <= 3:

        flash("You can't delete assignment, your School's Package doesn't supports Assignment deleting", category="Package Restriction")

        try:
            return redirect(url_for("teachers_actions.homeT"))
        except:
            return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

    else:
        try:
            if request.method == "POST":
                assignmentId = request.form['assignmentID']

                assignment = Assignment.query.get(assignmentId)
                if assignment:
                    if assignment.user_id == current_user.id:
                        db.session.delete(assignment)
                        db.session.commit()

                flash("Aassignment Deleted", category="Success")

                try:
                    return redirect(url_for("teachers_actions.homeT"))
                except:
                    return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

                return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)


        except:
            flash(f"Something went wrong.", category="Error occurred")


            try:
                return redirect(url_for("teachers_actions.homeT"))
            except:
                return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)

            return render_template("ROAS.html", pts=School.query.filter_by(id=current_user.SJI).first(), nts=retNotes()[0], pt=User.query.filter_by(id=(School.query.filter_by(id=current_user.SJI).first().user_id)).first() , uanf=abbreviatedName, uan=abbreviatedName(current_user.name), current_time=time, current_date=date, current_user=current_user, generatedCode=generateCode(), dateClean=ds)