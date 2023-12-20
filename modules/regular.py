from modules.kernel.register import BaseModule
from modules.models import Regular


class RegularModule(BaseModule):
    name = "Regular"
    path = ""
    table = Regular
    prefix = "/regular"
    tags = ["Regular Operations", ]


regular_router = RegularModule.router  # type: ignore
