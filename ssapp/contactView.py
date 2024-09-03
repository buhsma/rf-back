from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import resend
import environ


@api_view(["POST"])
@permission_classes([AllowAny])
def contactRelay(request):
    email = request.data.get("email")
    subject = request.data.get("subject")
    message = request.data.get("message")

    if email is None or subject is None or message is None:
        return Response({"error": "Invalid request"}, status=400)
    else:
        resend.api_key = environ.Env().str("RESEND_API_KEY")
        params = {
            "from": "contact@relayfox.com",
            "to": [environ.Env().str("RELAY_EMAIL")],
            "subject": "Ticket from " + email + ": " + subject,
            "text": "From: " + email + "\n\n" + message,
        }
        resend.Emails.send(params)
