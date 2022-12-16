import smtplib
from email.mime.text import MIMEText

def send_email():
    try:
        print('smtp.gmail.com')
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login('robertocarlos2022is2@gmail.com', 'xovoykuzzuuhqlbn')
        print('Conectado..')

        email_to = 'diegoespinola98@fpuna.edu.py'
        # Construimos el mensaje simple
        mensaje = MIMEText("""Este es el mensajede las narices""")
        mensaje['From'] = 'robertocarlos2022is2@gmail.com'
        mensaje['To'] = ", ".join(email_to)
        mensaje['Subject'] = "Tienes un correo"

        mailServer.sendmail('robertocarlos2022is2@gmail.com',
                            email_to,
                            mensaje.as_string())

        print('Correo enviado correctamente')
    except Exception as e:
        print(e)


send_email()
