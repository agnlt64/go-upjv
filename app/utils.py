from flask import jsonify
import re

UPJV_ID_REGEX = r'^[a-zA-Z][0-9]{8}$'
PASSWORD_REGEX = r'^(?=.*[a-zA-Z])(?!.*\s)(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
EMAIL_REGEX = r'^[a-zA-Z]+\.[a-zA-Z]+@([a-zA-Z0-9-]+\.)?u-picardie\.fr$'
PHONE_REGEX = r'^[0-9]{10}$'

def error(message: str):
    return jsonify({
        'success': False,
        'message': message
    })

def success(message: str):
    return jsonify({
        'success': True,
        'message': message
    })

def check_email(email: str):
    return re.match(EMAIL_REGEX, email)

def check_password(password: str):
    return re.match(PASSWORD_REGEX, password)

def check_upjv_id(upjv_id: str):
    return re.match(UPJV_ID_REGEX, upjv_id)

def check_phone(phone: str):
    return re.match(PHONE_REGEX, phone)
