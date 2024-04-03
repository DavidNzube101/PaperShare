from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(200), unique=True)
  password = db.Column(db.String(200))
  name = db.Column(db.String(200))
  school = db.Column(db.String(200))
  grade = db.Column(db.String(200))
  paidStatus = db.Column(db.String(200))
  activationID = db.Column(db.String(200))
  appPlan = db.Column(db.String(200))
  activationStatus = db.Column(db.String(200))
  POAS = db.Column(db.String(200))
  PlanType = db.Column(db.String(200))
  who = db.Column(db.String(200))
  age = db.Column(db.String(3))

  SCI = db.Column(db.Integer)#, db.ForeignKey('school.id'))
  SJI = db.Column(db.Integer)
  Slots = db.Column(db.Integer)

  assignment = db.relationship('Assignment', back_populates='user')
  ua = db.relationship('User_Assignment', back_populates='user')
  sc = db.relationship('School', back_populates='user')
  nt = db.relationship('Note', back_populates='user')
  
class School(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200))
  email = db.Column(db.String(200), unique=True)
  description = db.Column(db.String(500))
  link = db.Column(db.String(200), unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  user = db.relationship('User', back_populates='sc')
  

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200))
  content = db.Column(db.String(10000))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  user = db.relationship('User', back_populates='nt')

class Notification(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  content = db.Column(db.String(500))
  timestamp = db.Column(db.DateTime, default=func.now())
  adStatus = db.Column(db.String(500))

  sender = db.relationship('User', foreign_keys=[sender_id])
  recipient = db.relationship('User', foreign_keys=[recipient_id])


class User_Assignment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.String(100000))
  name = db.Column(db.String(200))
  email = db.Column(db.String(200))
  image = db.Column(db.String(200))
  image_path = db.Column(db.String(10000))
  date = db.Column(db.String(200))
  time = db.Column(db.String(200))
  code = db.Column(db.Integer)

  linkCode = db.Column(db.Integer, db.ForeignKey('code.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  uaCode = db.relationship('Code', back_populates='acode')
  user = db.relationship('User', back_populates='ua')


class Code(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  assID = db.Column(db.Integer, db.ForeignKey('assignment.id'))
  submittedAssID = db.Column(db.Integer())

  assignment = db.relationship('Assignment', back_populates='tcode')
  acode = db.relationship('User_Assignment', back_populates='uaCode')

  codeNumber = db.Column(db.Integer)

class Assignment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.String(100000))
  name = db.Column(db.String(200))
  image = db.Column(db.String(200))
  image_path = db.Column(db.String(10000))
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  deadlineDate = db.Column(db.String(200))
  deadlineTime = db.Column(db.String(200))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  code = db.Column(db.Integer)



  user = db.relationship('User', back_populates='assignment')
  tcode = db.relationship('Code', back_populates='assignment')