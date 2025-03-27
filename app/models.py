from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import LoginManager

login_manager = LoginManager()

#Lädt User Daten
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Definition User Tabelle
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)

    inventory_lists = db.relationship("InventoryList", backref="owner", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#Definition Inventarlisten Tabelle
class InventoryList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    fields = db.relationship("InventoryField", backref="inventory_list", cascade="all, delete", lazy=True)
    items = db.relationship("InventoryItem", backref="inventory_list", cascade="all, delete", lazy=True)

#Definition Inventarlistenfeld Tabelle
class InventoryField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey("inventory_list.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.String(20), nullable=False)  # text, number, image, boolean

#Definition Inventarlisteneintrag Tabelle
class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey("inventory_list.id"), nullable=False)
    data = db.Column(db.JSON, nullable=False)  # alle Felder als JSON gespeichert
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
