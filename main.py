from fastapi import FastAPI
from modules.user import user_router
from modules.token import token_router
from modules.cash import cash_router
from modules.group import group_router
from modules.regular import regular_router
from modules.stats import stats_router
from modules.operation import operation_router

from modules.kernel.register import run_modules

""" Init the fast-api application """
app = FastAPI()
""" Run the all modules, which we have created. """
run_modules()


""" Including all routers from modules. """
app.include_router(stats_router)
app.include_router(user_router)
app.include_router(operation_router)
app.include_router(cash_router)
app.include_router(token_router)
app.include_router(group_router)
app.include_router(regular_router)
