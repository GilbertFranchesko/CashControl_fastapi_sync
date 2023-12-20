from modules.kernel.register import BaseModule
from modules.models import Operation


class OperationModule(BaseModule):
    name = "Operation"
    path = ""
    table = Operation
    prefix = "/operation"
    tags = ["FinancialOperations", ]


operation_router = OperationModule.router
