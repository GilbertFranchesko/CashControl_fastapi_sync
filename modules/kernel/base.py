from piccolo.table import create_db_tables_sync
from piccolo.table import Table
from fastapi import APIRouter
from piccolo_api.fastapi.endpoints import FastAPIKwargs

import typing as t


class Module:

    def __init__(self,
                 name: str,
                 path: str,
                 tags: list,
                 table: Table,
                 prefix: t.Optional[str],
                 error_response: dict = {404: {"description": "Not found."}},
                 crud: bool = True,
                 api_kwargs: t.Optional[FastAPIKwargs] = None,
                 ) -> None:
        self._name = name
        self._path = path
        self._table = table
        self._prefix = str(prefix)
        self._tags = tags
        self._error_response = error_response

        self._crud = crud
        self._api_kwargs = api_kwargs

        self._router = t.Optional[APIRouter]

    def get_router(self):
        self._preproccesing()
        return self._router

    @property
    def path(self):
        return self._path

    @property
    def crud(self):
        return self._crud

    @property
    def api_kwargs(self):
        return self._api_kwargs

    @property
    def router(self):
        return self.get_router()

    @property
    def table(self):
        return self._table

    def get_table(self):
        return self._table

    def _init_table(self) -> None:
        create_db_tables_sync(self._table, if_not_exists=True)  # type: ignore

    def _conf_router(self) -> bool:
        self._router = APIRouter(
            prefix=self._prefix,
            tags=self._tags,
            responses=self._error_response
        )

        return True

    def _preproccesing(self):
        self._conf_router()
        if self._router is None:
            raise Exception("Router config error!")

    def run(self):
        self._preproccesing()
        self._init_table()
