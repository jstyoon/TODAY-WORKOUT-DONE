""" docstring """
from django.core.mail import EmailMessage


class Util:
    """ 별도 기능 클래스 """
    @staticmethod
    def send_email(data):
        """ EmailMessage 재정의 """
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()
