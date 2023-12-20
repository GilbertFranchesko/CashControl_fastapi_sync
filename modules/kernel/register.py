import typing as t
from .base import Module

from piccolo_api.fastapi.endpoints import FastAPIWrapper
from piccolo_api.crud.endpoints import PiccoloCRUD
from ..settings import MODULES

class RegistryModule(type):
    """
        The Singleton for saving all created modules.
    """
    registry: t.Dict = {}

    def __new__(cls, name, bases, dct):

        new_class = super().__new__(cls, name, bases, dct)

        """ 
            Checking for firstly object of "BaseModule".
            If yes, then we need the continue and not processing this object.
        """
        if (not dct.get("__qualname__") == "BaseModule") or (dct.get("crud", None) == False):
            args = cls._get_some_args(dct)
            new_class = Module(**args)
            cls.registry[name] = new_class
            return new_class
        else:
            return new_class

    @staticmethod
    def _get_some_args(dct: dict):
        """ Remove not needed keys

        Args:
            dct (dict): the dict with attributes of created object

        Returns:
            dict: the dict without needed keys
        """
        tmp_dct = dct

        # We not need this key
        tmp_dct.pop("__module__")
        # We not need this key
        tmp_dct.pop("__qualname__")

        return tmp_dct


class BaseModule(metaclass=RegistryModule):
    pass


def run_modules():
    """ The function for running all modules from registry.
    Returns:
        NONE
    """
    registry = RegistryModule.registry

    """
        Looking through all modules in registry.
    """
    print(MODULES)
    for module_name in MODULES:
        registry[module_name]._init_table()

        """ The checking attributes for running the module. """
        """
            1. If iteriable module not need the CRUD operations.
        """

        if registry[module_name].crud is False:
            pass

        else:
            FastAPIWrapper(
                    root_url=registry[module_name]._path,
                    fastapi_app=registry[module_name]._router,  # type: ignore
                    piccolo_crud=PiccoloCRUD(
                        table=registry[module_name]._table,  # type: ignore
                        read_only=False
                    ),
                    fastapi_kwargs=registry[module_name]._api_kwargs
                )
