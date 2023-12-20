from modules.schemas import GroupSchema
from .kernel.register import BaseModule
from .models import Group


class GroupModule(BaseModule):
    name = "Group"
    path = ""
    table = Group
    prefix = "/group"
    tags = ["Group", ]


group_router = GroupModule.router


def define_group(group: GroupSchema | int) -> GroupSchema:
    if isinstance(group, int):
        operation_group_db = Group.select() \
                    .where(Group.id == group).run_sync()  # type: ignore

        if len(operation_group_db) == 0 or operation_group_db is None:
            raise Exception("Group not found")

        operation_group = GroupSchema(**operation_group_db[0])

    else:
        try:
            tmp_group = GroupSchema(**group)
        except Exception as e:
            raise Exception(e)

        get_group_name = Group.select('name') \
                        .where(Group.name == tmp_group['name']).run_sync()

        if get_group_name is None:
            Group.insert(
                Group(**tmp_group)
            ).run_sync()

        operation_group_db = Group.select().where(Group.name == tmp_group['name']).run_sync()
        if len(operation_group_db) == 0 or operation_group_db is None:
            raise Exception("System created group not found.")

        operation_group = GroupSchema(**operation_group_db[0])

    return operation_group
