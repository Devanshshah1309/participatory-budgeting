from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    magic_link = db.Column(db.String(100), unique=True, nullable=False)
    has_voted = db.Column(db.Boolean, default=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)  # Optional description for the project
    cost = db.Column(db.Integer, nullable=True)

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    preference_value = db.Column(db.Boolean, default=False)  # True if the user is okay with the project

    user = db.relationship('User', backref=db.backref('preferences', lazy=True))
    project = db.relationship('Project', backref=db.backref('preferences', lazy=True))