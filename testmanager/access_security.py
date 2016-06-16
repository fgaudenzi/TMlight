from testmanager.model.user import User

def authenticate(username, password):
    user = User.query.filter_by(email=username).first()
    if user and user.verify_password(password):
        return user

def identity(payload):
    user_id = User.query.filter_by(id=payload['identity']).first()
    return user_id.id
