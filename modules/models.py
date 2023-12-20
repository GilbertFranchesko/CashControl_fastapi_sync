from db import DB
from piccolo.table import Table
from piccolo.columns import Varchar, Integer, Float, JSON, ForeignKey


class User(Table, db=DB):
    name = Varchar()
    hashed_password = Varchar()


class Operation(Table, db=DB):
    title = Varchar()
    user = ForeignKey(User)
    o_type = Varchar()
    cash = Float()
    comment = Varchar()


class Token(Table, db=DB):
    token = Varchar()
    user = Integer()


class Balance(Table, db=DB):
    current = Float()
    operations = JSON()


class Group(Table, db=DB):
    name = Varchar()
    limit = Float()
    current = Float()
    color = Varchar()


class Regular(Table, db=DB):
    name = Varchar()
    group = ForeignKey(Group)
    o_type = Varchar()
    cash = Float()
    r_type = Varchar()
