from flask import Blueprint, jsonify, request
from app.models import InventoryList, InventoryField, User
from werkzeug.security import check_password_hash

bp = Blueprint('api', __name__, url_prefix='/api')

#Abruf von User erstellte Inventarlisten
@bp.route("/list/<int:list_id>", methods=["GET"])
def api_get_list(list_id):
    auth = request.authorization
    if not auth:
        return jsonify({"error": "Authorization Required"}), 401

    user = User.query.filter_by(username=auth.username).first()
    if not user or not check_password_hash(user.password_hash, auth.password):
        return jsonify({"error": "Invalid Credentials"}), 403

    inv_list = InventoryList.query.get_or_404(list_id)
    if inv_list.user_id != user.id:
        return jsonify({"error": "Access denied"}), 403

    data = {
        "id": inv_list.id,
        "name": inv_list.name,
        "fields": [
            {"name": f.name, "type": f.field_type}
            for f in inv_list.fields
        ]
    }
    return jsonify(data)
