from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User
from werkzeug.security import generate_password_hash

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route("/")
@login_required
def show():
    return render_template("profile.html", user=current_user)

@bp.route("/edit", methods=["POST"])
@login_required
def edit():
    email = request.form.get("email")
    password = request.form.get("password")

    current_user.email = email
    if password:
        current_user.password_hash = generate_password_hash(password)
    db.session.commit()
    flash("Profil aktualisiert!", "success")
    return redirect(url_for("profile.show"))
