from app import db
from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime




class UserModel(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=True)
    phone = Column(String(11), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=True)
    password = Column(String(200), nullable=False)
    role = Column(Integer, nullable=False, default=2)
    code = Column(String(6), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    last_login = Column(DateTime, nullable=True)
    last_logout = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f'{self.id} :: {self.phone}'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        return self.role < 2


