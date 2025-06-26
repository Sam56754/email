import imaplib
import email
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from email.header import decode_header
import os


load_dotenv()
key = Fernet.generate_key()
fernet = Fernet(key)

load_dotenv()
password = os.getenv("PASSWORD").encode()

encrypted = fernet.encrypt(password)

# === CONFIGURATION ===
EMAIL = os.getenv("EMAIL")
PASSWORD = fernet.decrypt(encrypted, ttl=1).decode() # 1 second usage 
IMAP_SERVER = "imap.gmail.com"  # Change if not Gmail
IMAP_FOLDER = "INBOX"

# === Connect to Mail Server ===
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select(IMAP_FOLDER)

# === Search for All Emails ===
result, data = mail.search(None, 'ALL')
email_ids = data[0].split()

print(f"Total emails found: {len(email_ids)}\n")

# === Fetch and Display First 10 Emails ===
for num in email_ids[:10]:
    res, msg_data = mail.fetch(num, '(RFC822)')
    if res != 'OK':
        continue

    msg = email.message_from_bytes(msg_data[0][1])

    # Decode subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or 'utf-8', errors='ignore')

    # Decode sender
    from_ = msg.get("From")

    # Get date
    date_ = msg.get("Date")

    print(f"From: {from_}")
    print(f"Subject: {subject}")
    print(f"Date: {date_}\n")

mail.logout()
