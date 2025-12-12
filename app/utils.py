from flask import jsonify

from math import radians, sin, cos, sqrt, atan2
import re

from app.models.location import Location

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

def distance(from_: Location, to: Location) -> float:
    R = 6371.0
    lat1 = from_.lat
    lon1 = from_.lon
    lat2 = to.lat
    lon2 = to.lon

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def int_to_month(n: int) -> str:
    months = [
        "JAN", "FEV", "MAR", "AVR", "MAI", "JUN",
        "JUI", "AOUT", "SEP", "OCT", "NOV", "DEC"
    ]
    if 1 <= n <= 12:
        return months[n - 1]
    return ""