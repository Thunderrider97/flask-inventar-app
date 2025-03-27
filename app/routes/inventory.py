from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import InventoryList, InventoryField, InventoryItem
from app import db

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

#Definiert Hauptseite
@bp.route("/")
def home():
    return render_template("index.html")

#Zeigt alle selbst erstellten Inventarlisten an
@bp.route("/dashboard")
@login_required
def dashboard():
    lists = InventoryList.query.filter_by(user_id=current_user.id).all()
    return render_template("inventory_list.html", lists=lists)

#Zeigt die gewählte Inventarliste im Lesemodus an
@bp.route("/view/<int:list_id>")
@login_required
def view_list(list_id):
    inv_list = InventoryList.query.get_or_404(list_id)
    if inv_list.user_id != current_user.id:
        flash("Zugriff verweigert", "danger")
        return redirect(url_for("inventory.dashboard"))

    return render_template("manage_list.html", inv_list=inv_list)

#Erstellt eine neue Inventarliste
@bp.route("/new_list", methods=["GET", "POST"])
@login_required
def new_list():
    if request.method == "POST":
        name = request.form.get("list_name")
        field_names = request.form.getlist("field_name[]")
        field_types = request.form.getlist("field_type[]")

        inv_list = InventoryList(name=name, owner=current_user)
        db.session.add(inv_list)
        db.session.commit()

        for fname, ftype in zip(field_names, field_types):
            field = InventoryField(name=fname, field_type=ftype, list_id=inv_list.id)
            db.session.add(field)

        db.session.commit()
        flash("Liste erfolgreich erstellt!", "success")
        return redirect(url_for("inventory.dashboard"))

    return render_template("new_list.html")

#Zeigt Inventarliste im Bearbeitungsmodus an
@bp.route("/manage/<int:list_id>")
@login_required
def manage_list(list_id):
    inv_list = InventoryList.query.get_or_404(list_id)
    if inv_list.user_id != current_user.id:
        flash("Zugriff verweigert", "danger")
        return redirect(url_for("inventory.dashboard"))
    
    return render_template("manage_list.html", inv_list=inv_list)

#Neuen Eintrag im Inventarliste erstellen
@bp.route("/manage/<int:list_id>/add", methods=["GET", "POST"])
@login_required
def add_item(list_id):
    inv_list = InventoryList.query.get_or_404(list_id)
    if inv_list.user_id != current_user.id:
        flash("Zugriff verweigert", "danger")
        return redirect(url_for("inventory.dashboard"))

    if request.method == "POST":
        item_data = {}
        for field in inv_list.fields:
            value = request.form.get(field.name)
            if field.field_type == "boolean":
                item_data[field.name] = True if value == "on" else False
            else:
                item_data[field.name] = value

        item = InventoryItem(list_id=inv_list.id, data=item_data)
        db.session.add(item)
        db.session.commit()
        flash("Eintrag gespeichert!", "success")
        return redirect(url_for("inventory.manage_list", list_id=list_id))

    return render_template("add_item.html", inv_list=inv_list)

#Eintrag im Inventarliste bearbeiten
@bp.route("/manage/<int:list_id>/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(list_id, item_id):
    inv_list = InventoryList.query.get_or_404(list_id)
    item = InventoryItem.query.get_or_404(item_id)

    if inv_list.user_id != current_user.id or item.list_id != list_id:
        flash("Zugriff verweigert", "danger")
        return redirect(url_for("inventory.dashboard"))

    if request.method == "POST":
        for field in inv_list.fields:
            value = request.form.get(field.name)
            if field.field_type == "boolean":
                item.data[field.name] = True if value == "on" else False
            else:
                item.data[field.name] = value
        db.session.commit()
        flash("Eintrag aktualisiert!", "success")
        return redirect(url_for("inventory.manage_list", list_id=list_id))

    return render_template("edit_item.html", inv_list=inv_list, item=item)

#Eintrag in Inventarliste löschen
@bp.route("/manage/<int:list_id>/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_item(list_id, item_id):
    inv_list = InventoryList.query.get_or_404(list_id)
    item = InventoryItem.query.get_or_404(item_id)

    if inv_list.user_id != current_user.id or item.list_id != list_id:
        flash("Zugriff verweigert", "danger")
        return redirect(url_for("inventory.dashboard"))

    db.session.delete(item)
    db.session.commit()
    flash("Eintrag gelöscht.", "info")
    return redirect(url_for("inventory.manage_list", list_id=list_id))

#Inventarliste bearbeiten
@bp.route("/edit/<int:list_id>", methods=["GET", "POST"])
@login_required
def edit_list(list_id):
    inv_list = InventoryList.query.get_or_404(list_id)
    if inv_list.user_id != current_user.id:
        flash("Zugriff verweigert", "danger")
        return redirect(url_for("inventory.dashboard"))

    if request.method == "POST":
        inv_list.name = request.form.get("list_name")

        # Bestehende Felder aktualisieren
        for field in inv_list.fields:
            new_name = request.form.get(f"field_name_{field.id}")
            new_type = request.form.get(f"field_type_{field.id}")
            if new_name and new_type:
                field.name = new_name
                field.field_type = new_type

        # Neue Felder hinzufügen
        new_field_names = request.form.getlist("new_field_name[]")
        new_field_types = request.form.getlist("new_field_type[]")
        for name, ftype in zip(new_field_names, new_field_types):
            if name and ftype:
                new_field = InventoryField(name=name, field_type=ftype, list=inv_list)
                db.session.add(new_field)

        db.session.commit()
        flash("Liste aktualisiert!", "success")
        return redirect(url_for("inventory.dashboard"))

    return render_template("edit_list.html", inv_list=inv_list)

#Inventarliste löschen
@bp.route("/delete/<int:list_id>", methods=["POST"])
@login_required
def delete_list(list_id):
    inv_list = InventoryList.query.get_or_404(list_id)

    if inv_list.user_id != current_user.id:
        flash("Zugriff verweigert", "danger")
        return redirect(url_for("inventory.dashboard"))

    db.session.delete(inv_list)
    db.session.commit()
    flash("Liste gelöscht.", "info")
    return redirect(url_for("inventory.dashboard"))
