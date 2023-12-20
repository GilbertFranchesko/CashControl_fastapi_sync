from modules.schemas import UserSchema
from .kernel.register import BaseModule
from .models import Token
from .settings import SECRET_KEY, ALGORITHM

import jwt


class TokenModule(BaseModule):
    name = "Token"
    path = ""
    table = Token
    prefix = "/token"
    tags = ["Token", ]


token_router = TokenModule.router  # type: ignore
token_table = TokenModule.table  # type: ignore


def create_token(user: UserSchema):
    try:
        user_data = UserSchema(**user)
    except Exception as e:
        return e

    return jwt.encode(user_data, SECRET_KEY, ALGORITHM)


def decode_token(tok: str):
    token = Token.select().where(Token.token == tok).run_sync()  # type: ignore
    print(tok)
    if token[0] is None:
        return

    decode_jwt = jwt.decode(token[0]['token'], SECRET_KEY, [ALGORITHM,])
    return decode_jwt

def insert_token(token: str, user: int):
    token = Token.insert(
        Token(token=token, user=user)
    ).run_sync()
    print(token)
