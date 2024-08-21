import os
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core import mail
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'  # replace 'myproject.settings' with your project's settings

settings.configure()

def send_test_email(request):
    html_content = """
    <html>
        <body style="background-color: #35495e; text-align: center;">
            <div style="margin: auto; width: 50%;">
                <img src="http://localhost:5173/fox.png" alt="Logo" style="display: block; margin: auto;">
                <h1 style="color: #42b883;">Reset Password</h1>
                <p style="color: #42b883;">Click the link below to reset your password.</p>
            </div>
        </body>
    </html>
    """

    try:
        send_mail(
            'Subject here',
            'Here is the message.',
            'server@test.com',
            ['buhsma@gmail.com'],
            fail_silently=False,
            html_message=html_content,
        )
    except Exception as e:
        print(f"Error occurred: {e}")

    return HttpResponse('<br>'.join(str(msg) for msg in mail.outbox))