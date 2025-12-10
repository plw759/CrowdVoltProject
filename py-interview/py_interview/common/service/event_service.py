import abc
from typing import List, Optional, Tuple
from logging import getLogger

from py_interview.common.data_layer.event_data_layer import EventDataLayer
from py_interview.common.data_layer.comment_data_layer import CommentDataLayer
from py_interview.common.domain.event import EventDTO, event_to_dto, new_event
from py_interview.common.domain.comment import CommentDTO, comment_to_dto, new_comment

class EventService(metaclass=abc.ABCMeta):
    def get_events(self) -> List[EventDTO]:
        """
        gets all events

        :return: List[EventDTO]
        """

    def create_or_update_event(self, uqid: str, name: str, description: str,
                               img_link: str) -> EventDTO:
        """
        creates or updates events

        :param description:
        :param img_link:
        :param name:
        :param uqid:
        :return: EventDTO
        """

    def like_event(self, uqid: str) -> None:
        """
        likes an event

        :param uqid:
        :return: None
        """

    def get_comments(self, event_uqid: str, limit: int = 20, offset: int = 0) -> Tuple[List[CommentDTO], int]:
        """
        Gets comments for an event with offset-based pagination

        :param event_uqid: Event ID to get comments for
        :param limit: Number of comments to return (default 20, max 100)
        :param offset: Starting position (default 0)
        :return: Tuple of (comments, total_count)
        """

    def add_comment(self, event_uqid: str, user: str, text: str) -> CommentDTO:
        """
        adds a comment to an event

        :param event_uqid: Event ID to add comment to
        :param user: User adding the comment
        :param text: Text of the comment
        :return: The saved comment
        """

class EventServiceDefault(EventService):

    def __init__(self, event_data_layer: EventDataLayer, comment_data_layer: CommentDataLayer):
        self._event_data_layer = event_data_layer
        self._comment_data_layer = comment_data_layer
        self._logger = getLogger(self.__module__)

    def get_events(self) -> List[EventDTO]:
        return [event_to_dto(event) for event in self._event_data_layer.list()]

    def create_or_update_event(self, uqid: str, name: str, description: str,
                               img_link: str) -> EventDTO:
        if uqid is not None:
            event = self._event_data_layer.update(
                uqid=uqid, attr={'name': name, 'description': description,
                                 'img_link': img_link}
            )
        else:
            event = self._event_data_layer.create(
                new_event(name=name, description=description, img_link=img_link, number_of_likes=0)
            )

        return event_to_dto(event)

    def like_event(self, uqid: str) -> None:
        event = self._event_data_layer.get(uqid=uqid)

        self._event_data_layer.update(
            uqid=uqid, attr={'number_of_likes': event.number_of_likes + 1}
        )

    def get_comments(self, event_uqid: str, limit: int = 20, offset: int = 0) -> Tuple[List[CommentDTO], int]:
        """Get comments with offset pagination"""
        self._logger.info(f"Service: Getting comments for event {event_uqid}, limit={limit}, offset={offset}")
        comments, total_count = self._comment_data_layer.get_comments_for_event(event_uqid, limit, offset)
        self._logger.info(f"Service: Retrieved {len(comments)} comments, total={total_count}")
        return [comment_to_dto(c) for c in comments], total_count

    def add_comment(self, event_uqid: str, user: str, text: str) -> CommentDTO:
        self._logger.info(f"Service: Adding comment to event {event_uqid} by {user}: '{text[:50]}...'")
        comment = new_comment(event_uqid=event_uqid ,user=user, text=text)
        self._logger.info(f"Service: Created comment object with uqid={comment.uqid}")
        saved_comment = self._comment_data_layer.add_comment(event_uqid, comment)
        self._logger.info(f"Service: Comment saved successfully, saved_comment uqid={saved_comment.uqid}")
        return comment_to_dto(saved_comment) 
    
    def like_comment(self, comment_uqid: str) -> None:
        comment = self._comment_data_layer.get(uqid=comment_uqid)

        self._comment_data_layer.update(
            uqid=comment_uqid, attr={'number_of_likes': comment.number_of_likes + 1}
        )