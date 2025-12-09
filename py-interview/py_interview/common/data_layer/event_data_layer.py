import abc
from threading import Thread
from typing import Union, List, Optional, Dict, Any

from py_interview.common.domain.event import Event
from py_interview.common.helpers.base.base_data_layer import BaseDataLayer
from py_interview.common.helpers.base.base_data_layer_cache import BaseDataLayerCache
from py_interview.common.helpers.base.base_data_layer_in_memory import BaseDataLayerInMemory


class EventDataLayer(BaseDataLayer, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, obj: Union[Event, List[Event]]) -> Union[Event, List[Event]]:
        """
        Saves

        """

    @abc.abstractmethod
    def get(self, uqid: str = None, **kwargs) -> Optional[Event]:
        """

        """

    @abc.abstractmethod
    def list(self, uqid: str | List[str] = None, offset: int = 0, limit: int = None, **kwargs) -> List[Event]:
        """

        """

    @abc.abstractmethod
    def update(self, uqid: str, attr: Dict[str, Any], user: str = 'unknown') -> Optional[Event]:
        """

        """

    @abc.abstractmethod
    def delete(self, uqid: str) -> Optional[Event]:
        """

        """

class EventDataLayerInMemory(BaseDataLayerInMemory, EventDataLayer):
    def __init__(self):
        super(EventDataLayerInMemory, self).__init__(target_class=Event)

class EventDataLayerCache(BaseDataLayerCache, EventDataLayer, Thread):
    def __init__(self, underlying: EventDataLayer):
        BaseDataLayerCache.__init__(self, target_class=Event, underlying=underlying)
