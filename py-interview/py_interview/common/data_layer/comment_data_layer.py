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
        self._comments_by_event = {}  # type: dict
        self._logger = getLogger(self.__module__)

    def add_comment(self, event_uqid: str, comment: Comment) -> Comment:
        """
        Add a comment to an event

        :param event_uqid: Event ID
        :param comment: Comment to add
        :return: The saved comment
        """
        self._logger.info(f"CommentDataLayer: Adding comment to event {event_uqid}, comment uqid={comment.uqid}, user={comment.user}")
        if event_uqid not in self._comments_by_event:
            self._logger.info(f"CommentDataLayer: First comment for event {event_uqid}, creating list")
            self._comments_by_event[event_uqid] = []

        self._comments_by_event[event_uqid].append(comment)
        # Also store in base class dict by comment uqid for direct access
        self._data[comment.uqid] = comment
        self._logger.info(f"CommentDataLayer: Comment added. Event {event_uqid} now has {len(self._comments_by_event[event_uqid])} comments")
        return comment

    def get_comments_for_event(self, event_uqid: str, limit: int = 20, cursor: Optional[str] = None) -> Tuple[List[Comment], Optional[str]]:
        """
        Get comments for an event with cursor-based pagination

        :param event_uqid: Event ID
        :param limit: Number of comments to return
        :param cursor: Cursor (comment uqid) to start after
        :return: Tuple of (comments, next_cursor)
        """
        self._logger.info(f"CommentDataLayer: Getting comments for event {event_uqid}, limit={limit}, cursor={cursor}")
        comments = self._comments_by_event.get(event_uqid, [])
        self._logger.info(f"CommentDataLayer: Found {len(comments)} total comments for event {event_uqid}")

        # Find starting position
        start_idx = 0
        if cursor:
            # Find the comment with the cursor uqid and start after it
            for i, comment in enumerate(comments):
                if comment.uqid == cursor:
                    start_idx = i + 1
                    self._logger.info(f"CommentDataLayer: Found cursor at index {i}, starting from {start_idx}")
                    break

        # Get limit+1 to determine if there are more results
        end_idx = start_idx + limit + 1
        result_comments = comments[start_idx:end_idx]

        # Determine next cursor
        next_cursor = None
        if len(result_comments) > limit:
            next_cursor = result_comments[limit - 1].uqid
            result_comments = result_comments[:limit]
            self._logger.info(f"CommentDataLayer: Returning {limit} comments with next_cursor={next_cursor}")
        else:
            self._logger.info(f"CommentDataLayer: Returning {len(result_comments)} comments, no more available")

        return result_comments, next_cursor

