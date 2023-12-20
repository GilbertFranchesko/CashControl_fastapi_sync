from typing import Literal, Any, List

from typing_extensions import TypedDict


class UserSchema(TypedDict):
    id: int
    name: str
    hashed_password: str


class GroupSchema(TypedDict):
    id: int
    name: str
    color: Literal['red', 'yellow', 'orange']
    current: float
    limit: float


class RegularSchema(TypedDict):
    id: int
    name: str
    group: GroupSchema
    cash: float
    o_type: Literal['+', '-']
    r_type: Literal['monatly', "daily"]


class CashOperation(TypedDict):
    cash: float
    o_type: Literal['+', '-']
    group: GroupSchema | int


class Alert(TypedDict):
    a_type: Literal['limit']
    detail: str
    data: Any


class OperationStats(TypedDict):
    operations: List[CashOperation]
    summary: float


class StatisticsData(TypedDict):
    users: int

    current_balance: float
    groups: List[GroupSchema]
    
    operations_minus: OperationStats
    operations_plus: OperationStats
