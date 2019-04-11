import datetime

from flask_login import UserMixin

from flaskeddit import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    communities = db.relationship("Community", backref="user", lazy="dynamic")
    posts = db.relationship("Post", backref="user", lazy="dynamic")
    replies = db.relationship("Reply", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User (username='{self.username}')>"


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    posts = db.relationship(
        "Post", backref="community", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Community (name='{self.name}', description='{self.description}', date_created='{self.date_created}')>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    post = db.Column(db.Text, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey("community.id"), nullable=False)
    replies = db.relationship(
        "Reply", backref="post", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Post (title='{self.title}', post='{self.post}', date_created='{self.date_created}')>"


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.Text, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def __repr__(self):
        return f"<Reply (reply='{self.reply}', date_created='{self.date_created}')>"


class PostVotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)


class ReplyVotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey("reply.id"), nullable=False)
