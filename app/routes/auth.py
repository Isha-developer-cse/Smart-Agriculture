from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models.user import User
from ..utils.auth import create_token


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    payload = request.get_json() or {}
    if not payload.get("email") or not payload.get("password") or not payload.get("name"):
        return jsonify({"error": "name, email and password are required"}), 400
    if User.query.filter_by(email=payload["email"].lower()).first():
        return jsonify({"error": "email already registered"}), 409

    user = User(name=payload["name"], email=payload["email"].lower())
    user.set_password(payload["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"user": user.to_dict(), "token": create_token(user)}), 201


@auth_bp.post("/login")
def login():
    payload = request.get_json() or {}
    user = User.query.filter_by(email=(payload.get("email") or "").lower()).first()
    if not user or not user.check_password(payload.get("password") or ""):
        return jsonify({"error": "invalid email or password"}), 401
    return jsonify({"user": user.to_dict(), "token": create_token(user)})
