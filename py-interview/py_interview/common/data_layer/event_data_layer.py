import abc
from threading import Thread
from typing import Union, List, Optional, Dict, Any, Tuple
from logging import getLogger

from py_interview.common.domain.event import Event, Comment
from py_interview.common.helpers.base.base_data_layer import BaseDataLayer
from py_interview.common.helpers.base.base_data_layer_cache import BaseDataLayerCache
from py_interview.common.helpers.base.base_data_layer_in_memory import BaseDataLayerInMemory
from py_interview.common.data_layer.comment_data_layer import CommentDataLayer


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
    def __init__(self, comment_data_layer: CommentDataLayer = None):
        super(EventDataLayerInMemory, self).__init__(target_class=Event)
        # Inject CommentDataLayer for managing comments separately
        if comment_data_layer is None:
            from py_interview.common.data_layer.comment_data_layer import CommentDataLayerInMemory
            comment_data_layer = CommentDataLayerInMemory()
        self._comment_data_layer = comment_data_layer
        self._logger = getLogger(self.__module__)

    def get_comments(self, event_uqid: str, limit: int = 20, cursor: Optional[str] = None) -> Tuple[List[Comment], Optional[str]]:
        return self._comment_data_layer.get_comments_for_event(event_uqid, limit, cursor)

    def add_comment(self, event_uqid: str, comment: Comment) -> Comment:
        return self._comment_data_layer.add_comment(event_uqid, comment)


class EventDataLayerCache(BaseDataLayerCache, EventDataLayer, Thread):
    def __init__(self, underlying: EventDataLayer):
        BaseDataLayerCache.__init__(self, target_class=Event, underlying=underlying)
