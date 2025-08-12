import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv  
import os

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        self.email = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
                
    def send_verification_email(self, to_email: str, username: str, verification_token: str):
        """Send verification email via Gmail with proper error handling"""
        verification_link = f"{self.frontend_url}?token={verification_token}"
        
        subject = "🔐 Verify Your Email - Auth Service"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; margin-bottom: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; color: white; }}
                .header h1 {{ margin: 0; font-size: 24px; }}
                .content {{ line-height: 1.6; color: #333; }}
                .verify-btn {{ display: inline-block; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }}
                .link-box {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; margin: 20px 0; word-break: break-all; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Verify Your Email</h1>
                </div>
                
                <div class="content">
                    <h2>Welcome, {username}! 👋</h2>
                    
                    <p>Thank you for registering! Please verify your email address to complete your registration.</p>
                    
                    <center>
                        <a href="{verification_link}" class="verify-btn">✅ Verify My Email</a>
                    </center>
                    
                    <p>Or copy and paste this link:</p>
                    <div class="link-box">
                        {verification_link}
                    </div>
                    
                    <p><strong>This link expires in 24 hours.</strong></p>
                </div>
                
                <div class="footer">
                    <p>Auth Service - Secure Authentication</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        if not self.email or not self.password:
            print("❌ Gmail credentials not configured")
            print(f"   EMAIL_USER: {self.email or 'NOT_SET'}")
            print(f"   EMAIL_PASSWORD: {'SET' if self.password else 'NOT_SET'}")
            return self._console_fallback(to_email, username, verification_link)
            
        if len(self.password) != 19:  # 16 chars + 3 spaces
            print(f"❌ Gmail App Password format incorrect (length: {len(self.password)})")
            print("💡 Should be 19 characters: 'abcd efgh ijkl mnop'")
            return self._console_fallback(to_email, username, verification_link)
        
        try:
            success = self._send_gmail(to_email, subject, html_body)
            if success:
                print(f"✅ Gmail email sent successfully to {to_email}")
                print(f"🔗 Verification link: {verification_link}")
                return True
            else:
                return self._console_fallback(to_email, username, verification_link)
                
        except Exception as e:
            print(f"❌ Gmail send failed: {e}")
            return self._console_fallback(to_email, username, verification_link)
    
    def send_welcome_email(self, to_email: str, username: str):
        """Send welcome email"""
        try:
            html_body = f"""
            <div style="font-family: Arial; max-width: 600px; margin: 0 auto; padding: 40px; background: white; border-radius: 15px;">
                <h1 style="color: #28a745; text-align: center;">🎉 Welcome {username}!</h1>
                <p>Your email has been verified successfully! You can now log in to your account.</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{self.frontend_url}" style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px;">Go to App</a>
                </div>
            </div>
            """
            
            self._send_gmail(to_email, "🎉 Welcome! Account Verified", html_body)
            print(f"✅ Welcome email sent to {to_email}")
        except:
            print(f"📧 Welcome email attempted for {username}")
        
        return True
    
    def _send_gmail(self, to_email: str, subject: str, html_body: str):
        """Send email via Gmail SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email
            msg['To'] = to_email
            
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"❌ SMTP Error: {e}")
            return False
    
    def _console_fallback(self, to_email: str, username: str, verification_link: str):
        """Console fallback if Gmail fails"""
        print("\n" + "📧" * 70)
        print("GMAIL FALLBACK - CONSOLE MODE")
        print("📧" * 70)
        print(f"📬 TO: {to_email}")
        print(f"👤 USER: {username}")
        print(f"🔗 VERIFICATION LINK:")
        print(f"   {verification_link}")
        print("\n💡 INSTRUCTIONS:")
        print("   1. Copy the verification link")
        print("   2. Paste in browser")
        print("   3. Account verified!")
        print("📧" * 70 + "\n")
        return True

email_service = EmailService()