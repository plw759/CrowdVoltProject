from py_interview.common.helpers.base_api import BaseAPI
from py_interview.common.service.event_service import EventService

from py_interview.server.resources.event_resource import EventResource


class Api(BaseAPI):

    def __init__(self, event_service: EventService):
        BaseAPI.__init__(self)

        event_resource = EventResource(event_service=event_service)
        self.add_route('/api/event', event_resource)
        self.add_route('/api/event/like', event_resource, suffix='like')
        self.add_route('/api/event/comment', event_resource, suffix='comment')
        self.add_route('/api/event/comments', event_resource, suffix='comments')
        self.add_route('/api/event/comment/like', event_resource, suffix='like_comment')