import sys
from pathlib import Path

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password

        def send_email(processed_data, email, password, to_email):
            msg = MIMEMultipart()
            msg["From"] = email
            msg["To"] = to_email
            msg["Subject"] = "Processed Data Report"

            body = "Here is the processed data:"
            msg.attach(MIMEText(body, "plain"))

            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(processed_data.to_csv(index=False).encode())
            encoders.encode_base64(attachment)
            attachment.add_header(
                "Content-Disposition", 'attachment; filename="report.csv"'
            )
            msg.attach(attachment)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, to_email, text)
            server.quit()

            send_email(processed_data, email, password, to_email)
