from sqlalchemy import Column, Integer, String
from passlib.apps import custom_app_context as pwd_context
from testmanager.database import Base
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String(120), unique=True)
    password = Column(String(128), unique=True)

    def __init__(self, email, password=None):
        self.password = pwd_context.encrypt(password)
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.email)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


    def generate_auth_token(self, expiration = 600):
        s = Serializer("trentatre trentini", expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer("trentatre trentini")
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
