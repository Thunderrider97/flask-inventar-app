from flask import Blueprint, redirect, url_for

bp = Blueprint("main", __name__)
#Definiert Hauptseite
@bp.route("/")
def root():
    return redirect(url_for("auth.login"))
