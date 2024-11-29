import uuid

from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

migrate = Migrate()
db = SQLAlchemy()


class UserCart(db.Model):
    __tablename__ = 'user_cart'

    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    gender = db.Column(db.String)
    refrence_id = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()


class UserApp(db.Model):
    __tablename__ = "user_app"

    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    gender = db.Column(db.String)
    refrence_id = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()


class UserAppPostData(db.Model):

    __tablename__ = 'user_app_post_data'

    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    gender = db.Column(db.String)
    refrence_id = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()


class ParallelData(db.Model):

    __tablename__ = 'parallel'

    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    gender = db.Column(db.String)
    refrence_id = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()


class DailyDataDelete(db.Model):

    __tablename__ = 'daily_data_delete'

    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_date = db.Column(db.Date, nullable=False, unique=True)
    process_name = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=func.now())

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()


class Users(db.Model):

    __tablename__ = "internal_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    email = db.Column(db.String, nullable=False)
    is_staff = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now())

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    def __str__(self):
        return self.first_name

    def __repr__(self):
        return super().__repr__()


def insert_initial_data(app):

    with app.app_context():
        email = app.config.get("ADMIN_MAIL")
        _pass = app.config.get("PASS")
        _username = app.config.get("USERNAME")

        if not Users.query.filter(
                Users.username == _username,
                Users.email == email).first():

            user_inst = Users(
                first_name="ADMIN",
                is_admin=True,
                is_staff=True,
                is_verified=True,
                is_active=True,
                username=_username,
                email=email,
                password=generate_password_hash(_pass)

            )
            user_inst.save()
