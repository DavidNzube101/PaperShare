
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

import datetime as dt
from datetime import datetime

current_date = dt.date.today()
current_time = datetime.now().strftime("%H:%M")

@auth.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
      email = request.form.get('email')
      password = request.form.get('password')

      user = User.query.filter_by(email=email).first()
      if user:
          if check_password_hash(user.password, password):
            if user.who == 'Student':
                if user.POAS == "Pending":
                    # flash(f"Hello {user.name}, Your application has been declined by your preferred school. Try another school.", category='Declined')
                    # user.POAS = "Declined"
                    # db.session.commit()
                    return redirect(url_for('students_actions.studentGate'))
                elif user.POAS == "Joined":
                    flash(f"Welcome {user.name}", category='Success')
                    login_user(user, remember=True)
                    return redirect(url_for('students_actions.home'))
                elif user.POAS == "Declined":
                    flash(f"Welcome {user.name}", category='Success')
                    login_user(user, remember=True)
                    return redirect(url_for('students_actions.home'))
                else:
                    login_user(user, remember=True)
                    flash("To access this page, please join a school.", category="Important")
                    return redirect(url_for('students_actions.studentGate'))

            elif user.who == 'Teacher':
              if user.POAS == "Pending":
                  login_user(user, remember=True)
                  return redirect(url_for('teachers_actions.gateT'))
              elif user.POAS == "Joined":
                  flash(f"Welcome {user.name}", category='Success')
                  login_user(user, remember=True)
                  return redirect(url_for('teachers_actions.homeT'))
              elif user.POAS == "Declined":
                  flash(f"Welcome {user.name}", category='Success')
                  login_user(user, remember=True)
                  return redirect(url_for('teachers_actions.homeT'))
              else:
                  login_user(user, remember=True)
                  flash("To access this page, please join a school.", category="Important")
                  return redirect(url_for('teachers_actions.gateT'))
                  
            elif user.who == 'Admin':
              if user.PlanType == "Free":
                login_user(user, remember=True)   
                return redirect(url_for("views.redirectToChoosePlanForm"))
              else:  
                login_user(user, remember=True)
                return redirect(url_for("views.homeA"))
          else:
              flash("Incorrect password. Please try again.", category="Error occurred")
      else:
          flash("Email not found. Please register first.", category="Error occurred")
  return render_template('login.html')

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  flash("Logged out successfully.", category='Success')
  return redirect(url_for('auth.login'))

@auth.route("/signup", methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
      name = request.form.get('name')
      email = request.form.get('email')
      age = request.form.get('theage')
      # who = request.form.get('who')
      password1 = request.form.get('password')
      password2 = request.form.get('password2')

      user = User.query.filter_by(email=email).first()

      if user:
          flash("Email is already taken. Please use a different email.", category='Error occurred')
      elif len(email) < 4:
          flash('Invalid email: Email must be at least 4 characters long.', category='Error occurred')
      elif len(name) < 2:
          flash('Invalid name: Name must be at least 2 characters long.', category='Error occurred')
      elif password1 != password2:
          flash('Passwords do not match. Please re-enter your password.', category='Error occurred')
      elif len(password1) < 8:
          flash('Password is too short. It must be at least 8 characters long.', category='Error occurred')
      else:
          
          new_user = User(age=age, email=email, name=name, password=generate_password_hash(password1)) 

          db.session.add(new_user)
          db.session.commit()
          login_user(new_user, remember=True)

          try:
            return redirect(url_for("views.SAT"))
          except:
            return render_template("signup-choose-type.html", current_user=current_user, current_app=current_app)



  return render_template("signup.html")

