from flask import Blueprint, redirect, url_for

bp = Blueprint("main", __name__)

@bp.route("/")
def root():
    return redirect(url_for("auth.login"))
