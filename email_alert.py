# import smtplib
# import ssl

# def send_mail(to_email, product_title, current_price, product_url):
#     sender_email = "kamaljyotsingh@gmail.com"
#     app_password = "your_16_char_gmail_app_password"  # App password (no spaces)

#     subject = f"Price Drop Alert: {product_title}"
#     body = f"""\
# 📉 The price for "{product_title}" has dropped to ₹{current_price}!

# 👉 Check it out here: {product_url}

# You’re getting this alert because you asked to be notified when the price drops below your target.
# """

#     message = f"Subject: {subject}\n\n{body}"

#     try:
#         context = ssl.create_default_context()
        
#         # ✅ TLS on port 587 (not SSL)
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.ehlo()                         # Identify to server
#         server.starttls(context=context)     # Secure the connection
#         server.ehlo()                         # Re-identify after securing
#         server.login(sender_email, app_password)
#         server.sendmail(sender_email, to_email, message)
#         server.quit()
        
#         print("✅ Email sent successfully using TLS (Port 587)!")
#     except Exception as e:
#         print("❌ Failed to send email:", e)
import requests

MAILERSEND_API_KEY = "mlsn.56dd32ecc8db1bafa52daeb698a540bf872c02c1e6661e46e25b95b689f50f0e"
FROM_EMAIL = "test@test-ywj2lpnjkjkg7oqz.mlsender.net"

def send_mail(to_email, product_title, current_price, product_url):
    subject = f"Price Drop Alert: {product_title}"
    body = f"""
📉 The price for "{product_title}" has dropped to ₹{current_price}!

👉 Check it out here: {product_url}

You’re getting this alert because you asked to be notified when the price drops.
"""

    payload = {
        "from": {
            "email": FROM_EMAIL,
            "name": "Amazon Price Tracker"
        },
        "to": [
            {"email": to_email}
        ],
        "subject": subject,
        "text": body
    }

    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.mailersend.com/v1/email", json=payload, headers=headers)
        if response.status_code == 202:
            print("✅ Email sent successfully via MailerSend!")
        else:
            print(f"❌ MailerSend failed: {response.status_code} - {response.text}")
    except Exception as e:
        print("❌ Exception during email sending:", e)