import datetime
from domain.user import User

class LoginStatus:
    CREATED = 'CREATED'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'

class Token:
    def __init__(self, token: str, user: User):
        self.token = token
        self.user = User(user.name, user.id)
        self.created_at = datetime.datetime.now()
        self.status = LoginStatus.CREATED
        self.reset()
        
    def reset(self):
        self.last_login = datetime.datetime.now()
        self.login_count = 0
        self.expires_at = datetime.datetime.now() + datetime.timedelta(minutes=5)

    def set_status(self, status: str):
        self.status = status

    def get_token(self) -> str:
        return self.token
    
    def get_user(self) -> User:
        return self.user
    
    def get_user_id(self) -> int:
        return self.user.id
    
    def add(self):
        self.last_login = datetime.datetime.now()
        self.login_count += 1
        self.expires_at = datetime.datetime.now() + datetime.timedelta(minutes=5)

    def is_expired(self) -> bool:
        return self.expires_at < datetime.datetime.now()

    def ToJson(self):
        return {
            'token': self.token,
            'user': self.user.ToJson(),
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat(),
            'login_count': self.login_count,
            'expires_at': self.expires_at.isoformat(),
            'status': self.status
        }    