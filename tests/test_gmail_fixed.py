# test_gmail_fixed.py
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def test_gmail_step_by_step():
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    print("🔍 Gmail Configuration Test")
    print("=" * 40)
    print(f"Email: {email_user}")
    print(f"Password length: {len(email_password) if email_password else 0}")
    print(f"Password preview: {email_password[:4]}...{email_password[-4:] if email_password and len(email_password) > 8 else ''}")
    print()
    
    if not email_password or len(email_password) != 19:  # 16 chars + 3 spaces
        print("❌ App Password format is wrong!")
        print("💡 Should be 19 characters total (16 chars + 3 spaces)")
        print("💡 Example: 'abcd efgh ijkl mnop'")
        return False
    
    try:
        print("🔄 Step 1: Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        print("✅ Connected!")
        
        print("🔄 Step 2: Starting TLS...")
        server.starttls()
        print("✅ TLS started!")
        
        print("🔄 Step 3: Logging in...")
        server.login(email_user, email_password)
        print("✅ Login successful!")
        
        print("🔄 Step 4: Sending test email...")
        msg = MIMEText("Gmail test successful! 🎉")
        msg['Subject'] = "FastAPI Auth Test"
        msg['From'] = email_user
        msg['To'] = email_user
        
        server.send_message(msg)
        server.quit()
        
        print("✅ Test email sent!")
        print("📧 Check your inbox!")
        print("\n🎉 Gmail is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure 2FA is enabled")
        print("2. Generate new App Password")
        print("3. Copy password WITH spaces")
        print("4. Wait 5 minutes after enabling 2FA")
        return False

if __name__ == "__main__":
    test_gmail_step_by_step()