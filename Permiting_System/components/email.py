import smtplib
import ssl
import secrets
from email.message import EmailMessage
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.conf import settings
from auth_app.utils import URLBuilder


class SendEmailMixin:
    """
    A class to send various types of emails.

    Attributes:
        sender_email (str): The email address of the sender.
        password (str): The password for the sender's email account.
    """
    def __init__(self):
        """
        Initializes the SendEmail object with sender's email and password.
        """
        self.sender_email = settings.EMAIL_HOST_USER
        self.password = settings.EMAIL_HOST_PASSWORD

    def send_email(self, em, receiver_email):
        """
        Sends an email message to the specified recipient.

        Args:
            em (EmailMessage): The email message to be sent.
            receiver_email (str): The email address of the recipient.

        Raises:
            smtplib.SMTPAuthenticationError: If SMTP authentication fails.
            smtplib.SMTPException: If an error occurs while sending the email.
        """
        context = ssl.create_default_context()
        try:
            with (smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp):
                smtp.login(self.sender_email, self.password)
                smtp.sendmail(self.sender_email, receiver_email, em.as_string())
                print(f'Email sent successfully to {receiver_email}.')
        except smtplib.SMTPAuthenticationError:
            print('SMTP authentication failed. Please check your email credentials.')
        except smtplib.SMTPException as e:
            print(f'Error sending email: {e}')

    def send_rejection_email(self, request, reason, applicant_id, receiver_email):
        """
        Sends a rejection email to the specified recipient.

        Args:
            request: The Django request object.
            reason (str): The reason for rejection.
            applicant_id (int): The ID of the applicant.
            receiver_email (str): The email address of the recipient.
        """
        subject = 'Account Registration'

        em = EmailMessage()
        em['From'] = self.sender_email
        em['To'] = receiver_email
        em['Subject'] = subject

        url_builder = URLBuilder(request)
        url = url_builder.build_url('update_applicant_details', applicant_id=applicant_id)

        email_body = render_to_string(
            'applicant_rejection_email.html', {
                'subject': subject,
                'reason': reason,
                'url': url
            })

        em.set_content(f'', subtype='html')
        em.add_alternative(email_body, subtype='html')

        self.send_email(em, receiver_email)

    def send_approval_email(self, request, username, password, receiver_email):
        """
        Sends an approval email to the specified recipient.

        Args:
            request: The Django request object.
            username (str): The username for the new account.
            password (str): The password for the new account.
            receiver_email (str): The email address of the recipient.
        """
        subject = 'Account Registration Approved'

        em = EmailMessage()
        em['From'] = self.sender_email
        em['To'] = receiver_email
        em['Subject'] = subject

        url_builder = URLBuilder(request)
        url = url_builder.build_url('login')

        email_body = render_to_string(
            'applicant_approval_email.html', {
                'subject': subject,
                'username': username,
                'password': password,
                'url': url
            })

        em.set_content(f'', subtype='html')
        em.add_alternative(email_body, subtype='html')

        self.send_email(em, receiver_email)

    def send_otp_email(self, request, receiver_email):
        """
        Sends an OTP email to the specified recipient.

        Args:
            request: The Django request object.
            receiver_email (str): The email address of the recipient.
        """
        LENGTH_OF_OTP = 6
        otp = ''.join(secrets.choice('0123456789') for _ in range(LENGTH_OF_OTP))

        subject = 'Account Verification'

        otp_expiration_time = datetime.now() + timedelta(minutes=5)
        request.session['sent_otp'] = otp
        request.session['expiration_time'] = otp_expiration_time.strftime(
            '%Y-%m-%d %H:%M:%S')

        em = EmailMessage()
        em['From'] = self.sender_email
        em['To'] = receiver_email
        em['Subject'] = 'Login Confirmation'

        email_body = render_to_string('otpemail.html', {
            'subject': subject,
            'otp': otp,
            'expiration_time': otp_expiration_time.strftime(
                '%Y-%m-%d %H:%M:%S')
        })

        em.set_content(f'', subtype='html')
        em.add_alternative(email_body, subtype='html')

        self.send_email(em, receiver_email)

    def send_reset_password_email(self, request, receiver_email):
        """
        Sends a password reset email to the specified receiver email address.

        This method constructs and sends an email containing a link for the
        user to reset their password. The link includes the receiver's email
        address as a URL parameter.

        Args:
            request (HttpRequest): The HttpRequest object.
            receiver_email (str): The email address of the user who requested the password reset.
        """
        subject = 'Reset Password'

        em = EmailMessage()
        em['From'] = self.sender_email
        em['To'] = receiver_email
        em['Subject'] = subject

        url_builder = URLBuilder(request)
        url = url_builder.build_url('auth:index_reset_password', receiver_email=receiver_email)

        email_body = render_to_string(
            'reset_password_email.html', {
                'url': url,
                'subject': subject,
            })

        em.set_content(f'', subtype='html')
        em.add_alternative(email_body, subtype='html')

        self.send_email(em, receiver_email)

    def send_permit_email(self, request, receiver_email, permitId):
        """
        Sends a password reset email to the specified receiver email address.

        This method constructs and sends an email containing a link for the
        user to reset their password. The link includes the receiver's email
        address as a URL parameter.

        Args:
            request (HttpRequest): The HttpRequest object.
            receiver_email (str): The email address of the user who requested the password reset.
        """
        subject = 'Permit'

        em = EmailMessage()
        em['From'] = self.sender_email
        em['To'] = receiver_email
        em['Subject'] = subject

        url_builder = URLBuilder(request)
        url = url_builder.build_url('trader:permit', permitId=permitId)

        email_body = render_to_string(
            'permit_email.html', {
                'url': url,
                'subject': subject,
            })

        em.set_content(f'', subtype='html')
        em.add_alternative(email_body, subtype='html')

        self.send_email(em, receiver_email)
