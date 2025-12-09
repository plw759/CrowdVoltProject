from logging import getLogger
from dataclasses import asdict
from typing import Union, List, Optional, Dict, Any, Type, TypeVar

from py_interview.common.helpers.base.base_data_layer import BaseDataLayer
from py_interview.common.helpers.base.base import Base

T = TypeVar('T', bound=Base)


class BaseDataLayerInMemory(BaseDataLayer):

    def __init__(self, target_class: Type[T]):
        self._logger = getLogger(self.__module__)
        self._target_class = target_class
        self._data = {}  # type: dict[str, T]

    def create(self, obj: Union[T, List[T]]) -> Union[T, List[T]]:
        objs = [obj] if isinstance(obj, self._target_class) else obj
        res = []
        for obj in objs:
            self._data[obj.uqid] = obj
            res.append(obj)
        return res if len(res) > 1 else res[0]

    def get(self, uqid: str = None, **kwargs) -> Optional[T]:
        if uqid is None:
            raise Exception('uqid is none')
        if uqid is not None:
            return self._data.get(uqid, None)

    def list(self, uqid: str | List[str] = None, offset: int = 0, limit: int = None, **kwargs) -> List[T]:
        limit = limit or 1_000_000

        res = []
        values = list(self._data.values())  # type: List[T]

        for v in values:
            if uqid is not None:
                if isinstance(uqid, str):
                    if v.uqid != uqid:
                        continue
                else:
                    if v.uqid not in uqid:
                        continue
            bad_filter = False

            for key, value in kwargs.items():
                if key.endswith('s') and isinstance(value, list):
                    attr_name = key[:-1]
                    if attr_name not in self._target_class.__annotations__:
                        raise ValueError(f"{attr_name} is not an attribute of {self._target_class.__name__}")

                    if v.__getattribute__(attr_name) not in value:
                        bad_filter=True
                        break

                else:
                    if key not in self._target_class.__annotations__:
                        raise ValueError(f"{key} is not an attribute of {self._target_class.__name__}")
                    if v.__getattribute__(key) != value:
                        bad_filter = True
                        break
            if not bad_filter:
                res.append(v)

        return res[offset: offset + limit if offset + limit < len(res) else len(res) + 1]

    def update(self, uqid: str, attr: Dict[str, Any], user: str = 'unknown') -> Optional[T]:
        provider = self.get(uqid=uqid)
        updated_provider = self._target_class(**{**asdict(provider), **attr})
        self._data[uqid] = updated_provider
        return updated_provider

    def delete(self, uqid: str) -> Optional[T]:
        to_delete = self.get(uqid=uqid)
        if to_delete is None:
            return None

        del self._data[uqid]
        return to_delete
