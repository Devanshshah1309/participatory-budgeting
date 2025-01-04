import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(email, magic_link):
    message = Mail(
        from_email='admin@voteapp.com',
        to_emails=email,
        subject='Your Magic Link to Vote',
        html_content=f'Click <a href="http://localhost:5000/vote/{magic_link}">here</a> to vote.'
    )
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(str(e))