import abc
from typing import List, Optional, Tuple
from logging import getLogger

from py_interview.common.domain.comment import Comment
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
    def get_comments_for_event(self, event_uqid: str, limit: int = 20, offset: int = 0) -> Tuple[List[Comment], int]:
        """
        Get comments for an event with offset-based pagination

        :param event_uqid: Event ID to get comments for
        :param limit: Number of comments to return (default 20, max 100)
        :param offset: Starting position (0 = first comment)
        :return: Tuple of (comments, total_count)
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

    def get_comments_for_event(self, event_uqid: str, limit: int = 20, offset: int = 0) -> Tuple[List[Comment], int]:
        """
        Get comments for an event with offset-based pagination

        :param event_uqid: Event ID
        :param limit: Number of comments to return (default 20, max 100)
        :param offset: Starting position (0 = first comment)
        :return: Tuple of (comments, total_count)
        """
        # Validate inputs
        limit = max(1, min(limit, 100))  # Enforce 1-100 range
        offset = max(0, offset)  # Ensure offset is non-negative

        comment_uqids = self._comment_uqids_by_event.get(event_uqid, [])
        total_count = len(comment_uqids)
        
        self._logger.info(f"CommentDataLayer: Getting comments for event {event_uqid}, limit={limit}, offset={offset}, total={total_count}")
        
        # Get slice of UQIDs for this page
        paginated_uqids = comment_uqids[offset:offset+limit]
        
        # Fetch comment objects
        result_comments = [self._data.get(uqid) for uqid in paginated_uqids if uqid in self._data]
        
        self._logger.info(f"CommentDataLayer: Returned {len(result_comments)} comments, total available={total_count}")
        
        return result_comments, total_count

    def delete(self, uqid: str) -> Optional[Comment]:
        to_delete = super().get(uqid=uqid)
        if to_delete is None:
            return None

        event_uqid = to_delete.event_uqid 
        if event_uqid in self._comment_uqids_by_event:
            self._comment_uqids_by_event[event_uqid].remove(uqid)
        
        return super().delete(uqid=uqid)