import resend
import os

# Ideally, store your API key in an environment variable
resend.api_key = os.getenv("RESEND_API_KEY", "re_chwTgzjy_CeU8zdZJ3V8oW2qYhbMUhe7P")

def send_password_reset_email(user_email, token):
    reset_link = f"http://relayfox.com/reset-password/{token}/"
    
    # HTML version of the email
    html_content = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    </head>
    <body style="background-color: #35495e; margin: 0; padding: 0; width: 100%; font-family: 'Inter', sans-serif;">
        <table width="100%" height="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #35495e; height: 100vh; text-align: center;">
            <tr>
                <td align="center">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #1c2733; padding: 20px; border-radius: 10px;">
                        <tr>
                            <td style="text-align: left; vertical-align: middle; padding-right: 20px;">
                                <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                    <tr>
                                        <td style="text-align: left;">
                                            <p style="color: #42b883; margin: 0;">Click the link below to reset your password.</p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="text-align: center; padding-top: 10px;">
                                            <a href="{reset_link}" style="display: inline-block; background-color: #42b883; color: #000000; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                            <td style="text-align: right; vertical-align: middle;">
                                <img src="http://relayfox.com/fox.png" alt="Logo" style="max-width: 100px; height: auto;">
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>
    """
    
    plain_text_content = f"""
    Reset Your Password
    
    Click the link below to reset your password:
    
    {reset_link}
    
    If you did not request a password reset, please ignore this email.
    """

    params = {
        "from": "bro@relayfox.com",
        "to": [user_email],
        "subject": "Reset Password",
        "html": html_content,
        "text": plain_text_content, 
    }
    
    try:
        email = resend.Emails.send(params)
        print("Email sent successfully:", email)
    except Exception as e:
        print("An error occurred while sending the email:", str(e))

# send_password_reset_email("buhsma@gmail.com", "your-token-here")
