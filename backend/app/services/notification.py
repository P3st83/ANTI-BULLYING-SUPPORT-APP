from typing import List, Dict, Optional
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client as TwilioClient
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.sendgrid_client = None
        self.twilio_client = None
        
        if settings.SENDGRID_API_KEY:
            self.sendgrid_client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        else:
            logger.warning("SendGrid API key not configured")
            
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.twilio_client = TwilioClient(
                settings.TWILIO_ACCOUNT_SID, 
                settings.TWILIO_AUTH_TOKEN
            )
        else:
            logger.warning("Twilio credentials not configured")
    
    def send_email(self, to_email: str, subject: str, content: str, from_email: str = None) -> Dict:
        if not self.sendgrid_client:
            logger.warning("Email service not configured, simulating email send")
            return {
                "success": True,
                "message": f"Mock email sent to {to_email}",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        try:
            from_email = from_email or settings.FROM_EMAIL
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=content
            )
            
            response = self.sendgrid_client.send(message)
            
            return {
                "success": True,
                "message": "Email sent successfully",
                "status_code": response.status_code,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {
                "success": False,
                "message": f"Failed to send email: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def send_sms(self, to_phone: str, message: str) -> Dict:
        if not self.twilio_client:
            logger.warning("SMS service not configured, simulating SMS send")
            return {
                "success": True,
                "message": f"Mock SMS sent to {to_phone}",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        try:
            message = self.twilio_client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=to_phone
            )
            
            return {
                "success": True,
                "message": "SMS sent successfully",
                "sid": message.sid,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
            return {
                "success": False,
                "message": f"Failed to send SMS: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def send_emergency_alert(self, emergency_contacts: List[Dict], user_name: str, alert_type: str = "emergency") -> List[Dict]:
        results = []
        
        alert_subject = f"🚨 Emergency Alert for {user_name}"
        alert_message = f"""EMERGENCY ALERT
        
User: {user_name}
Alert Type: {alert_type}
Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

This is an automated alert from the Anti-Bullying Support App. 
Please check on {user_name} immediately.

If this is a life-threatening emergency, call 911.

For crisis support:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741"""
        
        for contact in emergency_contacts:
            if contact.get("email"):
                email_result = self.send_email(
                    to_email=contact["email"],
                    subject=alert_subject,
                    content=alert_message.replace('\n', '<br>')
                )
                results.append({
                    "contact": contact,
                    "method": "email",
                    "result": email_result
                })
            
            if contact.get("phone"):
                sms_result = self.send_sms(
                    to_phone=contact["phone"],
                    message=f"EMERGENCY ALERT: Please check on {user_name} immediately. If life-threatening, call 911. Time: {datetime.utcnow().strftime('%H:%M')}"
                )
                results.append({
                    "contact": contact,
                    "method": "sms", 
                    "result": sms_result
                })
        
        return results
    
    def send_parental_consent_email(self, parent_email: str, child_name: str, consent_link: str) -> Dict:
        subject = f"Parental Consent Required - {child_name} wants to join Anti-Bullying Support App"
        
        content = f"""
        <h2>Parental Consent Required</h2>
        
        <p>Hello,</p>
        
        <p>Your child, <strong>{child_name}</strong>, has requested to create an account on the Anti-Bullying Support App.</p>
        
        <p>This app provides:</p>
        <ul>
            <li>Safe, monitored emotional support</li>
            <li>Anonymous reporting of bullying incidents</li>
            <li>Educational resources about bullying prevention</li>
            <li>AI-powered chat support with safety monitoring</li>
        </ul>
        
        <p>We take child safety and privacy very seriously. All interactions are monitored for safety, and we comply with COPPA regulations.</p>
        
        <p><strong>To give your consent, please click the link below:</strong></p>
        <p><a href="{consent_link}" style="background-color: #6366f1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Give Parental Consent</a></p>
        
        <p>If you have any questions, please contact our support team.</p>
        
        <p>Best regards,<br>Anti-Bullying Support App Team</p>
        """
        
        return self.send_email(parent_email, subject, content)
    
    def send_report_notification(self, admin_email: str, report_details: Dict) -> Dict:
        subject = f"New Bullying Report Submitted - ID #{report_details.get('id', 'Unknown')}"
        
        content = f"""
        <h2>New Bullying Report Received</h2>
        
        <p><strong>Report Details:</strong></p>
        <ul>
            <li><strong>ID:</strong> #{report_details.get('id', 'Unknown')}</li>
            <li><strong>Type:</strong> {report_details.get('type', 'Unknown')}</li>
            <li><strong>Severity:</strong> {report_details.get('severity', 'Unknown')}/5</li>
            <li><strong>Anonymous:</strong> {'Yes' if report_details.get('is_anonymous') else 'No'}</li>
            <li><strong>Immediate Attention:</strong> {'YES' if report_details.get('requires_immediate_attention') else 'No'}</li>
            <li><strong>Submitted:</strong> {report_details.get('created_at', 'Unknown')}</li>
        </ul>
        
        <p><strong>Summary:</strong></p>
        <p>{report_details.get('description', 'No description provided')[:200]}...</p>
        
        <p>Please review this report in the admin dashboard as soon as possible.</p>
        
        <p>If marked as requiring immediate attention, please prioritize accordingly.</p>
        """
        
        return self.send_email(admin_email, subject, content)

notification_service = NotificationService()