from flask import Blueprint, request
from src.models import User, db
from http import HTTPStatus
from src.controllers.utils import requires_role
from flask_jwt_extended import jwt_required
from src.app import bcrypt

app = Blueprint("user", __name__, url_prefix="/users")



def _create_user():
    data = request.json
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
        )
    db.session.add(user)
    db.session.commit()

def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {"id": user.id,
         "username": user.username,
         "active": user.active,
         "role": {
             "id": user.role.id,
             "name": user.role.name,
         },
        } for user in users
    ]

@app.route("/<int:user_id>")
def user_details(user_id):
    user = db.get_or_404(User, user_id)
    return {"id": user.id,
         "username": user.username,
         "active": user.active,
         "role": {
             "id": user.role.id,
             "name": user.role.name,
         }}

@app.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_role("admin")
def handle_user():
    if request.method == "POST":
        _create_user()
        return {"Message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"Users": _list_users()}


@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    
    from sqlalchemy import inspect
    mapper = inspect(User)

    for column in mapper.attrs:
        if column.key in data: #column.key é o nome da chave que está sendo obtido do modelo. Ex: "username"
            setattr(user, column.key, data[column.key])
    db.session.commit()


    return {
        "id": user.id,
        "username": user.username,
        "active": user.active,
    }

@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT

@app.route("/test")
def test():
    return {"Users": _list_users()}