from fastapi.security import OAuth2PasswordBearer
from .models import Token, User
from .token import create_token
from .schemas import UserSchema

import hashlib

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


def hash_password(password: str):
    return hashlib.md5(password.encode())


def get_user(token: str):
    check_token = Token.select(Token.user).where(Token.token == token).run_sync()
    print(check_token)


def encode_token(data: UserSchema):
    create_token(data)


def decode_token(token: str) -> dict:
    print(User.select().where(User.name == token).run_sync()[0])
    return User.select().where(User.name == token).run_sync()[0]


