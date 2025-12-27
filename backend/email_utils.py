import os
import requests
from dotenv import load_dotenv

load_dotenv()

MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")
MAILTRAP_API_URL = "https://send.api.mailtrap.io/api/send"

def send_email(to_email, subject, text_content, html_content=None, from_name="WellWise Health"):
    """
    Send email using Mailtrap API
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        text_content (str): Plain text email content
        html_content (str, optional): HTML email content
        from_name (str): Sender name
    
    Returns:
        dict: API response or error
    """
    if not MAILTRAP_API_TOKEN:
        return {"error": "Mailtrap API token not configured"}
    
    payload = {
        "from": {
            "email": "hello@demomailtrap.com",
            "name": from_name
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "text": text_content,
        "category": "WellWise Notification"
    }
    
    if html_content:
        payload["html"] = html_content
    
    headers = {
        "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(MAILTRAP_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return {"status": "success", "message": "Email sent successfully"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}


def send_signup_notification(to_email, user_name, device_info):
    """
    Send signup confirmation email with device information
    
    Args:
        to_email (str): User's email
        user_name (str): User's name
        device_info (dict): Device information (browser, os, ip, location, timestamp)
    """
    browser = device_info.get('browser', 'Unknown Browser')
    os_name = device_info.get('os', 'Unknown OS')
    ip_address = device_info.get('ip', 'Unknown IP')
    location = device_info.get('location', 'Unknown Location')
    timestamp = device_info.get('timestamp', 'Just now')
    device_id = device_info.get('device_id', 'N/A')
    
    subject = "🎉 Welcome to WellWise - Account Created Successfully!"
    
    text = f"""
Hi {user_name},

Congratulations! Your WellWise account has been successfully created.

ACCOUNT DETAILS:
✅ Email: {to_email}
✅ Created: {timestamp}

DEVICE INFORMATION (for your security):
📱 Device: {browser} on {os_name}
🌍 Location: {location}
🔒 IP Address: {ip_address}
🆔 Device ID: {device_id}

If you did not create this account, please contact our support team immediately.

Get started with WellWise:
• Track your daily water intake
• Get personalized diet plans  
• Custom exercise recommendations
• AI-powered health predictions

Welcome aboard!

The WellWise Team
Smart AI Wellness Assistant
"""
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f3f4f6;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    
                    <!-- Header with gradient -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #22c55e 0%, #84cc16 100%); padding: 40px 30px; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 32px; font-weight: bold;">🎉 Welcome to WellWise!</h1>
                            <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 16px; opacity: 0.95;">Your journey to better health starts now</p>
                        </td>
                    </tr>
                    
                    <!-- Main content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6; color: #374151;">Hi <strong>{user_name}</strong>,</p>
                            
                            <p style="margin: 0 0 30px 0; font-size: 16px; line-height: 1.6; color: #374151;">
                                <strong>Congratulations!</strong> Your WellWise account has been successfully created. We're thrilled to have you join our community of health enthusiasts.
                            </p>
                            
                            <!-- Account Details Box -->
                            <div style="background: #f0fdf4; border-left: 4px solid #22c55e; padding: 20px; margin-bottom: 30px; border-radius: 8px;">
                                <h3 style="margin: 0 0 15px 0; color: #16a34a; font-size: 18px;">Account Created ✅</h3>
                                <p style="margin: 0 0 8px 0; color: #374151; font-size: 14px;"><strong>Email:</strong> {to_email}</p>
                                <p style="margin: 0; color: #374151; font-size: 14px;"><strong>Created:</strong> {timestamp}</p>
                            </div>
                            
                            <!-- Device Information Box -->
                            <div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 20px; margin-bottom: 30px; border-radius: 8px;">
                                <h3 style="margin: 0 0 15px 0; color: #2563eb; font-size: 16px;">🔒 Security Information</h3>
                                <p style="margin: 0 0 8px 0; color: #374151; font-size: 13px;"><strong>Device:</strong> {browser} on {os_name}</p>
                                <p style="margin: 0 0 8px 0; color: #374151; font-size: 13px;"><strong>Location:</strong> {location}</p>
                                <p style="margin: 0 0 8px 0; color: #374151; font-size: 13px;"><strong>IP Address:</strong> {ip_address}</p>
                                <p style="margin: 0; color: #374151; font-size: 13px;"><strong>Device ID:</strong> {device_id}</p>
                            </div>
                            
                            <!-- Features List -->
                            <h3 style="margin: 0 0 15px 0; color: #111827; font-size: 18px;">What you can do:</h3>
                            <ul style="margin: 0 0 30px 0; padding-left: 20px; color: #374151;">
                                <li style="margin-bottom: 10px;">💧 Track your daily water intake</li>
                                <li style="margin-bottom: 10px;">🥗 Get personalized diet plans</li>
                                <li style="margin-bottom: 10px;">💪 Custom exercise recommendations</li>
                                <li style="margin-bottom: 10px;">🤖 AI-powered health predictions</li>
                            </ul>
                            
                            <!-- CTA Button -->
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="http://localhost:5173/" style="display: inline-block; padding: 14px 32px; background: linear-gradient(135deg, #22c55e 0%, #84cc16 100%); color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">Get Started Now</a>
                            </div>
                            
                            <!-- Security Warning -->
                            <div style="background: #fff7ed; border: 1px solid #fdba74; padding: 15px; border-radius: 8px; margin-top: 30px;">
                                <p style="margin: 0; color: #9a3412; font-size: 13px;">
                                    ⚠️ <strong>Didn't sign up?</strong> If you did not create this account, please contact our support team immediately at <a href="mailto:support@wellwise.com" style="color: #ea580c;">support@wellwise.com</a>
                                </p>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f9fafb; padding: 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                            <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 14px;"><strong>WellWise</strong><br>Smart AI Wellness Assistant</p>
                            <p style="margin: 0; color: #9ca3af; font-size: 12px;">© 2025 WellWise. All rights reserved.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    
    return send_email(to_email, subject, text, html)


def send_login_notification(to_email, user_name, device_info):
    """
    Send login notification email with device and location information
    
    Args:
        to_email (str): User's email
        user_name (str): User's name
        device_info (dict): Device information (browser, os, ip, location, timestamp)
    """
    browser = device_info.get('browser', 'Unknown Browser')
    os_name = device_info.get('os', 'Unknown OS')
    ip_address = device_info.get('ip', 'Unknown IP')
    location = device_info.get('location', 'Unknown Location')
    timestamp = device_info.get('timestamp', 'Just now')
    device_id = device_info.get('device_id', 'N/A')
    
    subject = "🔐 New Login to Your WellWise Account"
    
    text = f"""
Hi {user_name},

We detected a new login to your WellWise account.

LOGIN DETAILS:
🕐 Time: {timestamp}
📱 Device: {browser} on {os_name}
🌍 Location: {location}
🔒 IP Address: {ip_address}
🆔 Device ID: {device_id}

If this was you, no action is needed. You can safely ignore this email.

⚠️ IF THIS WASN'T YOU:
This could mean someone else accessed your account. Please:
1. Change your password immediately
2. Review your account activity
3. Contact our support team

Secure your account: http://localhost:5173/login

Stay safe,
The WellWise Security Team
"""
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f3f4f6;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 40px 30px; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">🔐 New Login Detected</h1>
                            <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 14px; opacity: 0.95;">Security alert for your WellWise account</p>
                        </td>
                    </tr>
                    
                    <!-- Main content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6; color: #374151;">Hi <strong>{user_name}</strong>,</p>
                            
                            <p style="margin: 0 0 30px 0; font-size: 16px; line-height: 1.6; color: #374151;">
                                We detected a new login to your WellWise account. For your security, we're sending you this notification.
                            </p>
                            
                            <!-- Login Details Box -->
                            <div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 25px; margin-bottom: 25px; border-radius: 8px;">
                                <h3 style="margin: 0 0 20px 0; color: #1e40af; font-size: 18px;">📍 Login Information</h3>
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="padding: 8px 0; color: #6b7280; font-size: 14px; width: 120px;">🕐 Time:</td>
                                        <td style="padding: 8px 0; color: #111827; font-size: 14px; font-weight: 500;">{timestamp}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; color: #6b7280; font-size: 14px;">📱 Device:</td>
                                        <td style="padding: 8px 0; color: #111827; font-size: 14px; font-weight: 500;">{browser}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; color: #6b7280; font-size: 14px;">💻 OS:</td>
                                        <td style="padding: 8px 0; color: #111827; font-size: 14px; font-weight: 500;">{os_name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; color: #6b7280; font-size: 14px;">🌍 Location:</td>
                                        <td style="padding: 8px 0; color: #111827; font-size: 14px; font-weight: 500;">{location}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; color: #6b7280; font-size: 14px;">🔒 IP Address:</td>
                                        <td style="padding: 8px 0; color: #111827; font-size: 14px; font-weight: 500;">{ip_address}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; color: #6b7280; font-size: 14px;">🆔 Device ID:</td>
                                        <td style="padding: 8px 0; color: #111827; font-size: 14px; font-weight: 500; font-family: monospace;">{device_id}</td>
                                    </tr>
                                </table>
                            </div>
                            
                            <!-- Was this you? -->
                            <div style="background: #f0fdf4; border: 2px solid #22c55e; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
                                <h3 style="margin: 0 0 10px 0; color: #15803d; font-size: 16px;">✅ Was this you?</h3>
                                <p style="margin: 0; color: #166534; font-size: 14px; line-height: 1.6;">
                                    If you recognize this login, you can safely ignore this email. No further action is needed.
                                </p>
                            </div>
                            
                            <!-- Security Warning -->
                            <div style="background: #fef2f2; border: 2px solid #ef4444; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
                                <h3 style="margin: 0 0 15px 0; color: #991b1b; font-size: 16px;">⚠️ Wasn't you? Take action now!</h3>
                                <p style="margin: 0 0 15px 0; color: #7f1d1d; font-size: 14px; line-height: 1.6;">
                                    If you don't recognize this activity, your account may be compromised. Take these steps immediately:
                                </p>
                                <ol style="margin: 0; padding-left: 20px; color: #7f1d1d; font-size: 14px;">
                                    <li style="margin-bottom: 8px;">Change your password immediately</li>
                                    <li style="margin-bottom: 8px;">Review your recent account activity</li>
                                    <li>Contact our support team</li>
                                </ol>
                                <div style="text-align: center; margin-top: 20px;">
                                    <a href="http://localhost:5173/login" style="display: inline-block; padding: 12px 24px; background-color: #dc2626; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px;">Secure My Account</a>
                                </div>
                            </div>
                            
                            <p style="margin: 30px 0 0 0; color: #6b7280; font-size: 13px; line-height: 1.6;">
                                This is an automated security notification. We send these to help keep your account safe.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f9fafb; padding: 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                            <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 14px;"><strong>WellWise Security Team</strong><br>Smart AI Wellness Assistant</p>
                            <p style="margin: 0 0 10px 0; color: #9ca3af; font-size: 12px;">Need help? Contact us at support@wellwise.com</p>
                            <p style="margin: 0; color: #9ca3af; font-size: 12px;">© 2025 WellWise. All rights reserved.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    
    return send_email(to_email, subject, text, html)


def send_health_report_email(to_email, user_name, prediction_data):
    """Send health prediction report via email"""
    prediction = prediction_data.get('prediction', 'N/A')
    current_age = prediction_data.get('current_age', 'N/A')
    
    subject = "Your WellWise Health Report 📊"
    text = f"""
    Hi {user_name},

    Your health prediction is ready!

    Current Age: {current_age}
    Predicted Life Expectancy: {prediction} years

    View your full report at http://localhost:5173/

    Stay healthy,
    The WellWise Team
    """
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #22c55e;">Your WellWise Health Report 📊</h1>
            <p>Hi {user_name},</p>
            <p>Your health prediction is ready!</p>
            <div style="background: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p><strong>Current Age:</strong> {current_age}</p>
                <p><strong>Predicted Life Expectancy:</strong> <span style="font-size: 24px; color: #22c55e;">{prediction} years</span></p>
            </div>
            <a href="http://localhost:5173/" style="display: inline-block; margin-top: 20px; padding: 12px 24px; background: linear-gradient(to right, #22c55e, #84cc16); color: white; text-decoration: none; border-radius: 8px;">View Full Report</a>
            <p style="margin-top: 30px; color: #666;">Stay healthy,<br>The WellWise Team</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(to_email, subject, text, html)
