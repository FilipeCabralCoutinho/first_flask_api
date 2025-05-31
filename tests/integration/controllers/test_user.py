from http import HTTPStatus
from src.models.models import db, Role, User

def test_get_user_success(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="Batman", password="Batsenha", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    # When
    response = client.get("/users/1")

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"id": user.id,
         "username": user.username,
         "active": user.active,
         "role": {
             "id": user.role.id,
             "name": user.role.name,
         }}
    

def test_get_user_not_found(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user_id = 1

    # When
    response = client.get(f"/users/{user_id}")

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_list_users(client, access_token):
    # Given
    user = db.session.execute(db.select(User).where(User.username == "Batman")).scalar()

    response = client.post("/auth/login", json={"username": user.username, "password": user.password})
    access_token = response.json["access token"]



    # When
    response = client.get("/users/", headers={"Authorization": f"Bearer {access_token}"})

    # Then

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"Users": [
        {"id": user.id,
         "username": user.username,
         "active": user.active,
         "role": {
             "id": user.role.id,
             "name": user.role.name,
         },
        }
    ]}

def test_create_user(client, access_token):
    # Given
    role_id = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    payload = {"username":"Novo_usuario", "password": "1234", "role_id": role_id}

    # When
    response = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {access_token}"})

    # Then

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"Message": "User created!"}