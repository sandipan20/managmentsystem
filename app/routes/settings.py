"""
Settings and configuration routes for Hostel Manager
"""

from flask import Blueprint, render_template, request, jsonify
from app.routes.auth import login_required
from app.utils.email_service import get_email_config, save_email_config

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/email', methods=['GET', 'POST'])
@login_required
def email_settings():
    """Manage email configuration for sending reminders"""
    if request.method == 'POST':
        sender_email = request.form.get('sender_email', '').strip()
        sender_password = request.form.get('sender_password', '').strip()
        smtp_server = request.form.get('smtp_server', 'smtp.gmail.com').strip()
        smtp_port = request.form.get('smtp_port', '587').strip()
        
        if not sender_email or not sender_password:
            return render_template('settings/email.html',
                                 error='Email and password are required',
                                 config=get_email_config())
        
        success, message = save_email_config(sender_email, sender_password, smtp_server, smtp_port)
        
        if success:
            return render_template('settings/email.html',
                                 success='Email configuration saved successfully!',
                                 config=get_email_config())
        else:
            return render_template('settings/email.html',
                                 error=message,
                                 config=get_email_config())
    
    config = get_email_config()
    return render_template('settings/email.html', config=config)
