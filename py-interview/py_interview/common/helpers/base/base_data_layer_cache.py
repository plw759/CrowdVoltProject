from logging import getLogger
from typing import Union, List, Optional, Dict, Any, Type, TypeVar, Tuple
from cachetools import TTLCache
from time import sleep
from threading import Thread, RLock
from py_interview.common.helpers.base.base_data_layer import BaseDataLayer
from py_interview.common.helpers.base.base import Base

T = TypeVar('T', bound=Base)


class BaseDataLayerCache(BaseDataLayer, Thread):

    def __init__(self, target_class: Type[T],
                 underlying: BaseDataLayer,
                 ttl_secs: int = 60 * 10,
                 refresh_cache_secs: int = 60 * 10 - 20,
                 refresh_in_background: bool = True,
                 max_get_cache_size: int = 5000,
                 max_list_cache_size=150
                 ):
        Thread.__init__(self, daemon=True)
        self._logger = getLogger(self.__module__)
        self._target_class = target_class
        self._underlying = underlying
        self._ttl_secs = ttl_secs
        self._refresh_cache_secs = refresh_cache_secs
        self._refresh_in_background = refresh_in_background
        self._max_get_cache_size = max_get_cache_size
        self._max_list_cache_size = max_list_cache_size

        self._get_cache = TTLCache(maxsize=self._max_get_cache_size, ttl=ttl_secs)
        self._list_cache = TTLCache(maxsize=self._max_list_cache_size, ttl=ttl_secs)

        self._lock = RLock()

        if self._refresh_cache_secs and self._refresh_in_background:
            self.start()

    def run(self):
        while self._refresh_in_background:
            try:
                self.list()
            except Exception as _e:
                self._logger.exception("Issue loading cache")
            sleep(self._refresh_cache_secs)

    def create(self, obj: Union[T, List[T]]) -> Union[T, List[T]]:
        self._underlying.create(obj=obj)
        objs = [obj] if isinstance(obj, self._target_class) else obj
        with self._lock:
            for o in objs:
                self._get_cache[o.uqid] = o
            self._list_cache.clear()  # be safe
        return obj

    def get(self, uqid: str = None, **kwargs) -> Optional[T]:
        with self._lock:
            if uqid in self._get_cache:
                return self._get_cache[uqid]
            else:
                underlying = self._underlying.get(uqid=uqid)
                self._get_cache[uqid] = underlying
                return underlying

    def list(self, uqid: str | List[str] = None, offset: int = 0, limit: int = None, **kwargs) -> List[T]:
        limit = limit or 1_000_000

        with self._lock:
            key = f"{uqid}-{offset}-{limit}-{str(sorted(kwargs.items()))}"
            if key in self._list_cache:
                return self._list_cache[key]
            else:
                underlying = self._underlying.list(uqid=uqid, offset=offset, limit=limit, **kwargs)
                self._list_cache[key] = underlying
                for u in underlying:
                    self._get_cache[u.uqid] = u
                return underlying

    def update(self, uqid: str, attr: Dict[str, Any], user: str = 'unknown') -> Optional[T]:
        res = self._underlying.update(uqid=uqid, attr=attr, user=user)
        with self._lock:
            self._get_cache[res.uqid] = res
            self._list_cache.clear()  # be safe
        return res

    def delete(self, uqid: str) -> Optional[T]:
        res = self._underlying.delete(uqid=uqid)
        with self._lock:
            del self._get_cache[res.uqid]
            self._list_cache.clear()  # be safe
        return res
