from modules.schemas import UserSchema
from .models import User
from .kernel.register import BaseModule

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

from .auth import oauth2_scheme, hash_password
from .token import create_token, insert_token, decode_token

import typing as t


class UserModule(BaseModule):
    name = "User"
    path = ""
    table = User
    prefix = "/user"
    tags = ["User", ]


user_router = UserModule.router  # type: ignore
user_table = UserModule.table


def get_current_user(token: t.Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    print("Decoded: ", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@user_router.get("/me")
def me(
    current_user: t.Annotated[dict, Depends(get_current_user)]
):
    return current_user


@user_router.post("/token")
def login(form_data: t.Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_data = user_table.select() \
                    .where(user_table.name == form_data.username).run_sync()
    if not user_data:
        raise HTTPException(status_code=400, detail="auth failed")

    hashed_password = hash_password(form_data.password).hexdigest()

    try:
        user_data = UserSchema(**user_data[0])
    except Exception as e:
        return e

    if not hashed_password == user_data['hashed_password']:
        raise HTTPException(status_code=400, detail="auth failed")

    created_token = create_token(user_data)
    insert_token(created_token, user_data['id'])

    return {"access_token": created_token, "token_type": "bearer"}


@user_router.post("/register")
def register(name: str, password: str):
    user_data = user_table.select().where(user_table.name == name).run_sync()

    if len(user_data) >= 1:
        raise HTTPException(status_code=400, detail="Username already exists.")

    hashed_password = hash_password(password)
    user_table.insert(
        User(
            name=name,
            hashed_password=hashed_password.hexdigest()
        )
    ).run_sync()
