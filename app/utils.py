import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app

base_url = os.getenv('BASE_URL', 'http://localhost:5000')

def send_email(email, magic_link):
    message = Mail(
        from_email='admin@voteapp.com',
        to_emails=email,
        subject='Your Magic Link to Vote',
        html_content=f'Click <a href="{current_app.config['BASE_URL']}/vote/{magic_link}">here</a> to vote.'
    )
    try:
        sg = SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(str(e))