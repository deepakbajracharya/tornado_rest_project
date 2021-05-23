import tornado
import tornado.web as tweb
import json

from .service import WidgetService
from .app_util import widget2Dict
from .models import Widget


class WidgetHandler(tweb.RequestHandler):
    def initialize(self, engine: None):
        self.engine  = engine
        self.service = WidgetService(self.engine)

    async def get(self, widget_id):
        self.set_header("Content-Type", "application/json")
        widget = await self.service.findWidgetById(widget_id)
        self.write(json.dumps(widget2Dict(widget)))

    async def delete(self, widget_id):
        self.set_header("Content-Type", "application/json")
        await self.service.deleteWidgetById(widget_id)
        self.set_status(204)

    async def put(self, widget_id):
        self.set_header("Content-Type", "application/json")
        data   = tornado.escape.json_decode(self.request.body)
        widget = await self.service.updateWidget(widget_id, data=data)
        retData = widget2Dict(widget)
        self.write(tornado.escape.json_encode(retData))


class WidgetListHandler(WidgetHandler):

    async def get(self):
        self.set_header("Content-Type", "application/json")
        page      = self.get_argument("page", 1)
        page_size = self.get_argument("page_size", 50)
        lsWidgets = await self.service.listWidgets(
            page      = int(page),
            page_size = int(page_size)
        )
        txWidgets = [widget2Dict(x) for x in lsWidgets]
        wCount    = await self.service.widgetCount()
        retData   = {"data"      : txWidgets,
                     "count"     : wCount,
                     "page"      : page,
                     "page_size" : page_size
        }
        self.write(tornado.escape.json_encode(retData))

    async def post(self):
        data   = tornado.escape.json_decode(self.request.body)
        widget = Widget(
            name            = data["name"],
            number_of_parts = int(data["number_of_parts"])
        )
        await self.service.newWidget(widget)
        self.set_status(201)
        self.write(tornado.escape.json_encode(widget2Dict(widget)))
