import os
import time
from flask import Blueprint, request, jsonify, render_template, session, flash, redirect, url_for, current_app
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    set_access_cookies, unset_jwt_cookies, exceptions as jwt_exceptions
)
from werkzeug.security import generate_password_hash, check_password_hash
from util.utils import limpiar_carpetas

auth_bp = Blueprint('auth', __name__)

USER_DATA = {
    "username": os.getenv('ADMIN_USERNAME'),
    "password": generate_password_hash(os.getenv('ADMIN_PASSWORD'))
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify({"msg": "Faltan usuario o contraseña"}), 400

        if username != USER_DATA['username'] or not check_password_hash(USER_DATA['password'], password):
            return jsonify({"msg": "Credenciales inválidas"}), 401
        
        access_token = create_access_token(identity=username)
        response = jsonify(access_token=access_token)
        set_access_cookies(response, access_token)
        return response

    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "Cierre de sesión exitoso"})
    unset_jwt_cookies(response)
    session.clear()
    carpetas = ['video', 'audio', 'frames']
    time.sleep(0.5)
    limpiar_carpetas(carpetas)
    return response

@auth_bp.errorhandler(jwt_exceptions.NoAuthorizationError)
def handle_no_authorization_error(e):
    flash("No está autenticado. Por favor, inicie sesión.")
    return redirect(url_for('auth.login'))

@auth_bp.errorhandler(jwt_exceptions.WrongTokenError)
def handle_wrong_token_error(e):
    flash("Token de autorización inválido. Por favor, inicie sesión de nuevo.")
    return redirect(url_for('auth.login'))

@auth_bp.errorhandler(jwt_exceptions.RevokedTokenError)
def handle_revoked_token_error(e):
    flash("Token de autorización revocado. Por favor, inicie sesión de nuevo.")
    return redirect(url_for('auth.login'))
