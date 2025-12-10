from dataclasses import dataclass, asdict

from py_interview.common.helpers.base.base import Base, create_base

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