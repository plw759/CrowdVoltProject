import abc
from typing import List, Optional, Tuple
from logging import getLogger

from py_interview.common.domain.event import Comment
from py_interview.common.helpers.base.base_data_layer import BaseDataLayer
from py_interview.common.helpers.base.base_data_layer_in_memory import BaseDataLayerInMemory

class CommentDataLayer(BaseDataLayer, metaclass=abc.ABCMeta):
    """Abstract interface for comment storage operations"""

    @abc.abstractmethod
    def add_comment(self, event_uqid: str, comment: Comment) -> Comment:
        """
        Add a comment to an event

        :param event_uqid: Event ID to add comment to
        :param comment: Comment object to add
        :return: The saved comment
        """

    @abc.abstractmethod
    def get_comments_for_event(self, event_uqid: str, limit: int = 20, cursor: Optional[str] = None) -> Tuple[List[Comment], Optional[str]]:
        """
        Get comments for an event with cursor-based pagination

        :param event_uqid: Event ID to get comments for
        :param limit: Number of comments to return
        :param cursor: Cursor from previous response (comment uqid to start after)
        :return: Tuple of (comments, next_cursor)
        """


class CommentDataLayerInMemory(BaseDataLayerInMemory, CommentDataLayer):
    """In-memory implementation of comment storage"""

    def __init__(self):
        super(CommentDataLayerInMemory, self).__init__(target_class=Comment)
        # Maps event_uqid -> List[Comment]
        # WE cannot reuse base class _data dict because we need to group by event
        self._comment_uqids_by_event = {} # type: dict[str, List[str]]
        self._logger = getLogger(self.__module__)

    def add_comment(self, event_uqid: str, comment: Comment) -> Comment:
        """
        Add a comment to an event

        :param event_uqid: Event ID
        :param comment: Comment to add
        :return: The saved comment
        """  
        super().create(obj=comment) 

        if event_uqid not in self._comment_uqids_by_event:
            self._comment_uqids_by_event[event_uqid] = []
        
        self._comment_uqids_by_event[event_uqid].append(comment.uqid)

        return comment

    # TODO: use some sort of cursor-based or offset-based pagination
    # Have not decided which one to use yet or if really needed
    def get_comments_for_event(self, event_uqid: str, limit: int = None, offset: int = 0, cursor: Optional[str] = None) -> Tuple[List[Comment], Optional[str]]:
        """
        Get comments for an event 

        :param event_uqid: Event ID
        :param limit: Number of comments to return
        :param offset: Offset for pagination
        :param cursor: Cursor from previous response (comment uqid to start after)
        :return: Tuple of (comments, next_cursor)
        """
        limit = limit or 1_000_000

        comment_uqids = self._comment_uqids_by_event.get(event_uqid, [])
    
        ids_to_fetch = comment_uqids 
        
        result_comments = []
        
        for uqid in ids_to_fetch:
            if len(result_comments) >= limit:
                break
            comment = super().get(uqid=uqid) 
            if comment:
                result_comments.append(comment)
        
        return result_comments, None # No pagination implemented yet

    def delete(self, uqid: str) -> Optional[Comment]:
        to_delete = super().get(uqid=uqid)
        if to_delete is None:
            return None

        event_uqid = to_delete.event_uqid 
        if event_uqid in self._comment_uqids_by_event:
            self._comment_uqids_by_event[event_uqid].remove(uqid)
        
        return super().delete(uqid=uqid)