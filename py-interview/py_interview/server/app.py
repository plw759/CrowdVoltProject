import logging
from wsgiref.simple_server import make_server

from py_interview.common.data_layer.comment_data_layer import CommentDataLayerInMemory
from py_interview.common.data_layer.event_data_layer import EventDataLayerCache, EventDataLayerInMemory
from py_interview.common.domain.event import new_comment, new_event
from py_interview.common.service.event_service import EventServiceDefault
from py_interview.server.api import Api

# Logger set up
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

event_data_layer = EventDataLayerCache(EventDataLayerInMemory())
comment_data_layer = CommentDataLayerInMemory()

# save a sample one
event_data_layer.create(new_event(
    name='Test Event', description='Pokemon Stadium Tournament',
    img_link='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGg117hTNrhTBDkX0CTSHEnp7LRdOsrl76CQ&s',
    number_of_likes=0))

comment_data_layer.add_comment(
    event_uqid=event_data_layer.list()[0].uqid,
    comment=new_comment(event_uqid=event_data_layer.list()[0].uqid,
        text='Test Comment', user='First Comment',
        number_of_likes=0))

event_service = EventServiceDefault(event_data_layer=event_data_layer, comment_data_layer=comment_data_layer)

app = Api(event_service=event_service)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()