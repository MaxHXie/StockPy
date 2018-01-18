from django.core.mail import EmailMultiAlternatives

def send_template_mail(plaintext_template="", html_template="", context="", subject="", from_email="", to=""):
    try:
        text_content = plaintext_template.render(context)
        html_content = html_template.render(context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return True

    except:
        return False
