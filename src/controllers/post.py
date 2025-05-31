from flask import Blueprint, request
from src.models import Post, db
from http import HTTPStatus

app = Blueprint("post", __name__, url_prefix="/posts")

def _create_post():
    data = request.json
    post = Post(title=data["title"], body=data["body"], author_id=data["author_id"])
    db.session.add(post)
    db.session.commit()

def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [
        {"id": post.id,
         "title": post.title,
         "body": post.body,
         "created": post.created,
          "author_id": post.author_id }
         for post in posts
    ]

@app.route("/<int:post_id>")
def post_details(post_id):
    post = db.get_or_404(Post, post_id)
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id 
        }

@app.route("/", methods=["GET", "POST"])
def handle_post():
    if request.method == "POST":
        _create_post()
        return {"Message": "Post created!"}, HTTPStatus.CREATED
    else:
        return {"Posts": _list_posts()}


@app.route("/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json
    
    from sqlalchemy import inspect
    mapper = inspect(Post)

    for column in mapper.attrs:
        if column.key in data: #column.key é o nome da chave que está sendo obtido do modelo. Ex: "title"
            setattr(post, column.key, data[column.key])
    db.session.commit()


    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "created": post.created,
        "author_id": post.author_id 
        }

@app.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT