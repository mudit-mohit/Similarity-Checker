import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_similarity_result_email(recipient_email, similarity_score, explanation):
    sender_email = "your-email@example.com"
    sender_password = "your-email-password"

    subject = "Similarity Checker Report"
    body = f"""
    <h2>Similarity Score: {similarity_score:.2f}</h2>
    <p><strong>Explanation:</strong></p>
    <p>{explanation}</p>
    """

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False