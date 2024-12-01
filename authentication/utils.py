from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            data["email_subject"], data["email_body"], to=[data["to_email"]]
        )
        email.send()
