from flaskeddit import db
from flaskeddit.models import Post, Reply, ReplyVote


def get_reply(reply_id):
    reply = Reply.query.get(reply_id)
    return reply


def create_reply(reply, post, app_user):
    """Creates a new reply."""
    reply = Reply(reply=reply, post=post, app_user=app_user)
    db.session.add(reply)
    db.session.commit()


def update_reply(reply, reply_text):
    """Updates a reply."""
    reply.reply = reply_text
    db.session.commit()


def delete_reply(reply):
    """Deletes a reply."""
    db.session.delete(reply)
    db.session.commit()


def upvote_reply(reply_id, user_id):
    reply_vote = ReplyVote.query.filter_by(user_id=user_id, reply_id=reply_id).first()
    if reply_vote is None:
        reply_vote = ReplyVote(vote=1, user_id=user_id, reply_id=reply_id)
        db.session.add(reply_vote)
    elif abs(reply_vote.vote) == 1:
        reply_vote.vote = 0
    else:
        reply_vote.vote = 1
    db.session.commit()


def downvote_reply(reply_id, user_id):
    reply_vote = ReplyVote.query.filter_by(user_id=user_id, reply_id=reply_id).first()
    if reply_vote is None:
        reply_vote = ReplyVote(vote=-1, user_id=user_id, reply_id=reply_id)
        db.session.add(reply_vote)
    elif abs(reply_vote.vote) == 1:
        reply_vote.vote = 0
    else:
        reply_vote.vote = -1
    db.session.commit()
