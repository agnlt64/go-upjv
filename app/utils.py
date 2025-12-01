from flask import jsonify

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
