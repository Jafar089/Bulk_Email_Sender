import streamlit as st
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email
def send_email(sender_email, sender_password, receiver_email, subject, body):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server (for Gmail, use 'smtp.gmail.com' and port 587)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)  # Log in to the email account
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email

        st.success(f"Email sent to {receiver_email}")
    except Exception as e:
        st.error(f"Failed to send email to {receiver_email}: {e}")

# Function to read emails from CSV and send the email
def send_emails_from_csv(csv_file, sender_email, sender_password, subject, body):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        emails = df.iloc[:, 0].tolist()  # Assuming the email is in the first column

        # Send emails to all addresses
        for email in emails:
            send_email(sender_email, sender_password, email, subject, body)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")

# Streamlit App
def main():
    st.title("📧 Bulk Email Sender")

    # Instructions for App Password
    st.sidebar.header("Instructions")
    st.sidebar.write("""
    1. Enable **Two-Factor Authentication (2FA)** on your Google Account.
    2. Generate an **App Password** from your Google Account.
    3. Use the App Password in the app (not your regular Gmail password).
    """)

    # Input your email credentials
    st.sidebar.header("Email Credentials")
    sender_email = st.sidebar.text_input("Your Email Address")
    sender_password = st.sidebar.text_input("Your App Password", type="password")

    # Upload CSV file
    st.header("Upload CSV File")
    csv_file = st.file_uploader("Upload a CSV file containing email addresses", type=["csv"])

    # Input the email subject and body
    st.header("Compose Email")
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Body")

    # Send emails button
    if st.button("Send Emails"):
        if not sender_email or not sender_password:
            st.error("Please enter your email credentials.")
        elif csv_file is None:
            st.error("Please upload a CSV file.")
        elif not subject or not body:
            st.error("Please enter the email subject and body.")
        else:
            with st.spinner("Sending emails..."):
                send_emails_from_csv(csv_file, sender_email, sender_password, subject, body)
            st.success("All emails sent successfully!")

if __name__ == "__main__":
    main()