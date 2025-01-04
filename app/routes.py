from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models import User, Project, UserPreference
from app import db
from app.utils import send_email
import uuid
import pandas as pd

admin_bp = Blueprint('admin', __name__)
vote_bp = Blueprint('vote', __name__)
results_bp = Blueprint('results', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'upload_users':
            file = request.files['file']
            if file:
                df = pd.read_csv(file)
                for _, row in df.iterrows():
                    magic_link = str(uuid.uuid4())
                    user = User(name=row['name'], email=row['email'], magic_link=magic_link)
                    db.session.add(user)
                    db.session.commit()
                    send_email(row['email'], magic_link)
                flash('Magic links sent successfully!', 'success')
            csv_input = request.form.get('csv_input')
            if csv_input:
                entries = [entry.strip().split(',') for entry in csv_input.splitlines()]
                for name, email in entries:
                    magic_link = str(uuid.uuid4())
                    user = User(name=name, email=email, magic_link=magic_link)
                    db.session.add(user)
                    db.session.commit()
                    send_email(email, magic_link)
                flash('Magic links sent successfully for entered users!', 'success')


        elif action == 'upload_projects':
            file = request.files['project_file']
            if file:
                df = pd.read_csv(file)
                for _, row in df.iterrows():
                    project_name = row['name']
                    description = row.get('description', '')  # Optional description
                    if project_name:
                        project = Project(project_name=project_name, description=description)
                        db.session.add(project)
                db.session.commit()
                flash('Projects uploaded successfully!', 'success')
            csv_input = request.form.get('csv_input')
            if csv_input:
                entries = [entry.strip().split(',') for entry in csv_input.splitlines()]
                for name, description in entries:
                    if name:  # Ensure name is not empty
                        project = Project(project_name=name, description=description.strip())
                        db.session.add(project)
                db.session.commit()
                flash('Projects uploaded successfully from input!', 'success')

    users = User.query.all()
    projects = Project.query.all()
    user_preferences = UserPreference.query.all()

    # send some stats to be displayed too
    project_votes = {project.id: 0 for project in projects}
    total_votes = sum([1 if u.has_voted else 0 for u in users])
    for preference in user_preferences:
        if preference.preference_value:
            project_votes[preference.project_id] += 1

    # Prepare data for the chart
    project_names = [project.project_name for project in projects]
    project_percentages = [
        (project_votes[project.id] / total_votes * 100) if total_votes > 0 else 0
        for project in projects
    ]

    return render_template('admin.html', users=users, projects=projects, user_preferences=user_preferences, project_names=project_names, project_percentages=project_percentages,
                           users_count=len(users),
                           users_submitted_count=total_votes)

@vote_bp.route('/vote/<magic_link>', methods=['GET', 'POST'])
def vote(magic_link):
    user = User.query.filter_by(magic_link=magic_link).first()
    if user and not user.has_voted:
        print(request.form)
        if request.method == 'POST':
            projects = Project.query.all()  # Fetch all projects
            for project in projects:
                preference_value = request.form.get(f'project_{project.id}', '0') == '1'
                user_preference = UserPreference(user_id=user.id, project_id=project.id, preference_value=preference_value)
                db.session.add(user_preference)
            user.has_voted = True  # Mark user as having voted
            db.session.commit()
            return redirect(url_for('vote.thank_you'))
        else:
            projects = Project.query.all()  # Fetch all projects to display
            return render_template('vote.html', projects=projects, user=user)
    else:
        return "Error: Invalid or used link!"

@vote_bp.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@results_bp.route('/admin/results')
def admin_results():
    votes = UserPreference.query.all()
    return render_template('results.html', votes=votes)