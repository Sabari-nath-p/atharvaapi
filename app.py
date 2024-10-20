import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)

class SendEmail(Resource):
    def post(self):
        try:
            # Gmail credentials
            sender_email = "atharvacempunnapra@gmail.com"
            sender_password = "mwijcptdevuvggzk"  # Or app-specific password
            receiver_email = request.form['to']
            subject = request.form['subject']
            body = request.form['body']

            # Create a MIME message object
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach the email body
            msg.attach(MIMEText(body, 'plain'))

            # If an attachment is provided, attach it
            if 'attachment' in request.files:
                file = request.files['attachment']
                filename = file.filename

                # Save the file temporarily
                file.save(filename)

                # Open the file and attach it to the email
                attachment = open(filename, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                msg.attach(part)

                # Remove the temporarily saved file
                attachment.close()
                os.remove(filename)

            # Set up the Gmail server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()

            return jsonify({'message': 'Email sent successfully!'})

        except Exception as e:
            return jsonify({'error': str(e)})

api.add_resource(SendEmail, '/send-email')

if __name__ == '__main__':
    app.run(debug=True)
