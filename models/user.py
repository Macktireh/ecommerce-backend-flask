from datetime import datetime

from flask_login import UserMixin

from app import db, flask_bcrypt


# user_userImage = db.Table(
#         'user_userImage',
#         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#         db.Column('userImage_id', db.Integer, db.ForeignKey('userImage.id'))
#     )


class User(db.Model, UserMixin):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicId = db.Column(db.Text, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    firstName = db.Column(db.String(128))
    lastName = db.Column(db.String(128))
    isActive = db.Column(db.Boolean, nullable=False, default=False)
    isStaff = db.Column(db.Boolean, nullable=False, default=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    passwordHash = db.Column(db.Text, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('userImage.id'))
    # picture = db.relationship('UserImage', secondary=user_userImage, backref='users')


    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password: str):
        self.passwordHash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return flask_bcrypt.check_password_hash(self.passwordHash, password)

    def get_full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    def __repr__(self):
        return "<User '{}'>".format(self.email)


class UserImage(db.Model):
    """ UserImage Model for profile picture registration """
    __tablename__ = "userImage"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicId = db.Column(db.Text, unique=True)
    image = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    nimeType = db.Column(db.Text, nullable=False)
    user = db.relationship('User', uselist=False, backref='image')