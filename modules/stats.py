from modules.models import Balance, Operation, User, Group
from modules.schemas import StatisticsData

from .kernel.register import BaseModule


class StatsModule(BaseModule):
    name = "Stats"
    path = ""
    table = Balance
    prefix = "/stats"
    tags = ["Statistics", ]


stats_router = StatsModule.router


@stats_router.get("/")
def show_stats():
    num_users = len(User.select().run_sync())

    groups = Group.select().run_sync()

    current_balance = Balance.select().run_sync()[0]

    minus_operations = Operation.select().where(Operation.o_type == "-").run_sync()
    plus_operations = Operation.select().where(Operation.o_type == "+").run_sync()

    minus_summary = 0.0
    for operation in minus_operations:
        minus_summary = minus_summary + operation['cash']

    plus_summary = 0.0
    for operation in plus_operations:
        plus_summary = plus_summary + operation['cash']

    stats_data: StatisticsData = {
        "users": num_users,
        "currrent_balance": current_balance['current'],
        "groups": groups,
        "operation_minus": {
            "operations": minus_operations,
            "summary": minus_summary,
        },
        "operation_plus": {
            "operations": plus_operations,
            "summary": plus_summary,
        }
    }

    return stats_data
