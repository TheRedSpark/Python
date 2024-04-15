import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from package import variables
from package import mail_data

emails = mail_data.emails
betreffzeilen = mail_data.betreffzeilen

# E-Mail-Konfiguration
smtp_server = 'mail.gmx.net'
smtp_port = 587
email_address = variables.mail_from
email_password = variables.mail_password

# Zufällige Auswahl von E-Mail-Body und Betreffzeile
selected_email = random.choice(emails)
selected_subject = random.choice(betreffzeilen)

# E-Mail erstellen
message = MIMEMultipart()
message['From'] = email_address
message['To'] = mail_data.mail_to_remote
message['Cc'] = mail_data.mail_cc_me
message['Subject'] = selected_subject

message.attach(MIMEText(selected_email, 'plain'))

# Alle Empfänger für das Senden zusammenführen (To und Cc)
recipients = [message['To'], message['Cc']]

# SMTP-Server verbinden und E-Mail senden
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # Sicherheitsprotokoll aktivieren
server.login(email_address, email_password)
text = message.as_string()
server.sendmail(email_address, recipients, text)  # Empfängerliste zum Senden verwenden
server.quit()

print("E-Mail wurde erfolgreich gesendet!")