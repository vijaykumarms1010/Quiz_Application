from flask_login import UserMixin

from quizer import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    question_added = db.relationship("Question", backref="user", lazy=True, passive_deletes=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Question(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String(10000), nullable=False)
    answer = db.Column(db.String(10000), nullable=True)
    option1 = db.Column(db.String(10000), nullable=True)
    option2 = db.Column(db.String(10000), nullable=True)
    option3 = db.Column(db.String(10000), nullable=True)
    option4 = db.Column(db.String(10000), nullable=True)
    user_added = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    users_answered= db.Column(db.PickleType,nullable=True)
    def __repr__(self):
        return f"Question('{self.id}' '{self.ques}','{self.user_added}', '{self.users_answered}')"