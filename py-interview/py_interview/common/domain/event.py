import datetime
from dataclasses import dataclass, asdict

from py_interview.common.helpers.base.base import Base, create_base

@dataclass(frozen=True,kw_only=True, slots=True)
class Comment(Base):
    user: str
    text: str
    number_of_likes: int
    event_uqid: str
    def __as_dict__(self, path: dict, **kwargs):
        for key in path.keys():
            if key in self.__slots__:
                yield key, getattr(self, key)
            elif key in Base.__slots__:
                yield key, getattr(Base, key)
            elif hasattr(self, key):
                atr = getattr(self, key)
                yield key, atr(**kwargs)


@dataclass(frozen=True, kw_only=True, slots=True)
class Event(Base):
    name: str
    description: str
    img_link: str
    number_of_likes: int

    def __as_dict__(self, path: dict, **kwargs):
        for key in path.keys():
            if key in self.__slots__:
                yield key, getattr(self, key)
            elif key in Base.__slots__:
                yield key, getattr(Base, key)
            elif hasattr(self, key):
                atr = getattr(self, key)
                yield key, atr(**kwargs)


def new_event(name: str = 'unit-test-1', img_link: str = 'unit-test-1',
              number_of_likes: int = 0, description: str = 'unit-test-1',
              user: str = 'unit-test-1') -> Event:
    return Event(name=name, img_link=img_link, description=description,
                 number_of_likes=number_of_likes,
                 **asdict(create_base(user=user)))

def new_comment(event_uqid: str, user: str = 'unit-test-1', text: str = 'unit-test-1', number_of_likes: int = 0) -> Comment:
    return Comment(event_uqid=event_uqid, user=user, text=text, number_of_likes=number_of_likes, **asdict(create_base(user=user)))

@dataclass(slots=True)
class EventDTO:
    uqid: str
    name: str
    description: str
    img_link: str
    number_of_likes: int


def event_to_dto(event: Event) -> EventDTO: # Do Not return all comments with event
    return EventDTO(name=event.name, description=event.description, img_link=event.img_link,
                    number_of_likes=event.number_of_likes, uqid=event.uqid)

@dataclass(slots=True)
class CommentDTO:
    uqid: str
    event_uqid: str
    user: str
    text: str
    number_of_likes: int
    created_at: str

def comment_to_dto(comment: Comment) -> CommentDTO:
    return CommentDTO(uqid=comment.uqid, event_uqid=comment.event_uqid, user=comment.user, text=comment.text, number_of_likes=comment.number_of_likes, created_at=comment.created_at.isoformat())