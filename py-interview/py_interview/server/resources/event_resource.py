import dataclasses as dc
import json
from logging import getLogger

import falcon

from py_interview.common.service.event_service import EventService


class EventResource:

    def __init__(self, event_service: EventService):
        self._event_service = event_service
        self._logger = getLogger(self.__module__)

    def on_get(self, req, resp):
        events = self._event_service.get_events()

        resp.status = falcon.HTTP_200  # This is the default status
        resp.media = [dc.asdict(event) for event in events]

    def on_post(self, req, resp):
        post_body = json.load(req.bounded_stream)
        uqid = post_body.get('uqid', None)
        name = post_body.get('name', None)
        description = post_body.get('description', None)
        img_link = post_body.get('img_link', None)

        data = self._event_service.create_or_update_event(
            uqid=uqid, name=name, description=description, img_link=img_link)

        resp.status = falcon.HTTP_200  # This is the default status
        resp.media = dc.asdict(data)

    def on_post_like(self, req, resp):
        post_body = json.load(req.bounded_stream)
        uqid = post_body.get('uqid', None)

        self._event_service.like_event(uqid=uqid)
        resp.media = {'success': True}

        resp.status = falcon.HTTP_200  # This is the default status

    def on_post_comment(self, req, resp):
        self._logger.info("Resource: POST /api/event/comment - Add comment request received")
        post_body = json.load(req.bounded_stream)
        event_uqid = post_body.get('uqid', None) # id of event
        user = post_body.get('user', None)
        text = post_body.get('text', None)
        
        self._logger.info(f"Resource: Parsed request - event_uqid={event_uqid}, user={user}, text_length={len(text) if text else 0}")
        comment = self._event_service.add_comment(event_uqid=event_uqid, user=user, text=text)
        self._logger.info(f"Resource: Comment added successfully, comment uqid={comment.uqid}")
        resp.media = {'success': True, 'comment_uqid': comment.uqid}

        resp.status = falcon.HTTP_200  # This is the default status


    def on_get_comments(self, req, resp):
        self._logger.info("Resource: GET /api/event/comments - Get comments request received")
        event_uqid = req.get_param('uqid')
        limit = int(req.get_param('limit', default=20))
        offset = int(req.get_param('offset', default=0))
        
        self._logger.info(f"Resource: Parsed request - event_uqid={event_uqid}, limit={limit}, offset={offset}")
        comments, total_count = self._event_service.get_comments(event_uqid=event_uqid, limit=limit, offset=offset)
        self._logger.info(f"Resource: Retrieved {len(comments)} comments, total={total_count}")

        resp.status = falcon.HTTP_200
        resp.media = {
            'comments': [dc.asdict(comment) for comment in comments],
            'pagination': {
                'offset': offset,
                'limit': limit,
                'total': total_count,
                'has_more': (offset + limit) < total_count
            }
        }
        
    def on_post_like_comment(self, req, resp):
        post_body = json.load(req.bounded_stream)
        comment_uqid = post_body.get('comment_uqid', None)

        self._event_service.like_comment(comment_uqid=comment_uqid)

        resp.media = {'success': True}

        resp.status = falcon.HTTP_200  # This is the default status