from fastapi import HTTPException, Depends
from modules.group import define_group
from modules.schemas import CashOperation, GroupSchema
from modules.user import get_current_user
from .models import Balance, Group, Operation
from .kernel.register import BaseModule

import typing as t


class CashModule(BaseModule):
    name = "Cash"
    path = ""
    table = Balance
    prefix = "/cash"
    tags = ["Cash", ]


cash_router = CashModule.router  # type: ignore
cash_table = CashModule.table

"""
    Adding operation
"""


@cash_router.post("/operation")
def create_operation(form_operation: CashOperation,
                     current_user: t.Annotated[dict, Depends(get_current_user)]):
    try:
        operation_data = CashOperation(**form_operation)
    except Exception as e:
        print(e)
        raise Exception("Not defined args.")

    operation_data['group'] = define_group(form_operation['group'])

    current_balance = Balance.select().run_sync()[0]

    tmp_group_current = operation_data['group']['current']
    group_limit = operation_data['group']['limit']
    # TODO: To create a notify table and save this.
    if tmp_group_current + operation_data['cash'] > group_limit:
        pass

    if operation_data['o_type'] == "-":
        group_cash = float(operation_data['group']['current']) + float(operation_data['cash'])
        Group.update({Group.current: group_cash}).where(Group.id == operation_data['group']['id']).run_sync()

    some_balance = check_operations(
        operation_data['o_type'],
        current_balance['current'],
        operation_data['cash']
    )

    if some_balance is None:
        raise Exception("TMP CASH NONE")

    Balance.update({Balance.current: some_balance}).where(Balance.id == current_balance['id']).run_sync()
    Operation.insert(
        Operation(
            title="empty",
            user=current_user['id'],
            o_type=operation_data['o_type'],
            cash=float(operation_data['cash']),
            comment="Empty"
        )
    ).run_sync()

    get_operations_by_user = Operation.select().where(Operation.user == current_user['id']).run_sync()
    return get_operations_by_user


"""
    Check operation valid for current balance
"""


def check_operations(o_type, current_balance: float,
                     operation_cash: float) -> float:
    tmp_cash = 0.0

    if o_type == '-':
        tmp_cash = float(current_balance - operation_cash)
        if tmp_cash < 0:
            raise HTTPException(status_code=400, detail="Не хватает денег")

    if o_type == '+':
        tmp_cash = float(current_balance + operation_cash)

    return tmp_cash
